import json
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
import numpy as np

def create_prom_client_dict(config_filename):
    data = load_case_config(config_filename)
    prom_client_dict = {}
    for prom_url in data:
        prom = PrometheusConnect(url = prom_url, disable_ssl=True)
        prom_client_dict[prom_url] = prom
        
    return prom_client_dict

def load_case_config(config_filename):
    with open(config_filename, 'r') as f:
        data = json.load(f)

    return data['prom_url']

def cpu_avg_utilization(prom, start_time, end_time):
    start_time = parse_datetime(start_time)
    end_time = parse_datetime(end_time)
    # query= "sum by () (node_cpu_seconds_total{mode!='idle'})"
    query= "sum by (instance) (node_cpu_seconds_total{mode!='idle'})"
    metric_data = prom.custom_query_range(
        query = query,
        start_time=start_time,
        end_time=end_time,
        step = '1s'
    )
    result = {}
    for data in metric_data:
        val = data['values']
        cpu_used_time = float(val[-1][1]) - float(val[0][1])
        cpu_total_time = float(val[-1][0]) - float(val[0][0])
        instance_url = data["metric"]["instance"]
        if "prometheus-node-exporter" in instance_url:
            instance_url = prom.prometheus_host.split(':')[0]
        result[instance_url] = cpu_used_time/cpu_total_time * 100
    
    return result

def memory_avg_utilization(prom, start_time, end_time):
    start_time = parse_datetime(start_time)
    end_time = parse_datetime(end_time)
    # query = "1 - (node_memory_MemFree_bytes + node_memory_Cached_bytes + node_memory_Buffers_bytes) / node_memory_MemTotal_bytes"
    query = "node_memory_MemTotal_bytes - (node_memory_MemFree_bytes + node_memory_Cached_bytes + node_memory_Buffers_bytes)"
    metric_data = prom.custom_query_range(
        query = query,
        start_time=start_time,
        end_time=end_time,
        step = '1s'
    )
    result = {}
    for data in metric_data:
        val = data['values']
        arr = np.array(val)[:,1].astype('float')
        instance_url = data["metric"]["instance"]
        if "prometheus-node-exporter" in instance_url:
            instance_url = prom.prometheus_host.split(':')[0]
        result[instance_url] = np.average(arr) / 1024 / 1024

    return result

def invocation_count(prom, start_time, end_time):
    start_time = parse_datetime(start_time)
    end_time = parse_datetime(end_time)
    query = "sum by (function_name) (gateway_function_invocation_total{code='200'})"
    metric_data = prom.custom_query_range(
        query = query,
        start_time=start_time,
        end_time=end_time,
        step = '1s'
    )
    result = {}
    for data in metric_data:
        val = data['values']
        function_name = data["metric"]["function_name"]
        count = int(val[-1][1]) - int(val[0][1])
        result[function_name] = count

    return result