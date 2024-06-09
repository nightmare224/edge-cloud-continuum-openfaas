import argparse
from locustfile.runner import run
from prometheus.metrics import cpu_avg_utilization, memory_avg_utilization, create_prom_client_dict
from datetime import datetime
from time import sleep

if __name__ == "__main__":
    ### parse argument ###
    parser=argparse.ArgumentParser()
    parser.add_argument("-l", "--config-locust", type=str, default="./config/config_locust.json", help = "Path to the config file (default ./config_locust.json)")
    parser.add_argument("-p", "--config-prom", type=str, default="./config/config_prom.json", help = "Path to the config file (default ./config_locust.json)")
    parser.add_argument("-c", "--casename", type=str, required = True, help = "The target test case name in the config file")
    args = parser.parse_args()

    ### run workload by locust ###
    print(f"Running test case '{args.casename}'...")
    start_time = datetime.now()
    run(args.config_locust, args.casename)
    end_time = datetime.now()
    print("\nDone")

    ### gather resource metric from prometheus ###
    prom_client_dict = create_prom_client_dict(args.config_prom)
    metrics_dict = {}
    for url in prom_client_dict:
        metrics_dict[url] = {}
        # cpu
        cpu = cpu_avg_utilization(prom_client_dict[url], start_time, end_time)
        metrics_dict[url]['cpu'] = cpu
        # memory
        memory = memory_avg_utilization(prom_client_dict[url], start_time, end_time)
        metrics_dict[url]['memory'] = memory
        
    print(metrics_dict)