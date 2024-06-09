import json
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime


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
    query= "sum by () (node_cpu_seconds_total{mode!='idle'})"
    metric_data = prom.custom_query_range(
        query = query,
        start_time=start_time,
        end_time=end_time,
        step = '1s'
    )
    val = metric_data[0]['values']
    cpu_used_time = float(val[-1][1]) - float(val[0][1])
    cpu_total_time = float(val[-1][0]) - float(val[0][0])

    return cpu_used_time/cpu_total_time * 100

def memory_avg_utilization(prom, start_time, end_time):
    pass

# print(cpu_avg_utilization(prom, start_time, end_time))