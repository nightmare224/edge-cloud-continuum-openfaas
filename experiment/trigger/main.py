import argparse
import json
import os
import shutil
import glob
import pandas as pd
from locustfile.runner import run
from prometheus.metrics import cpu_avg_utilization, memory_avg_utilization, create_prom_client_dict
from datetime import datetime
from time import sleep

if __name__ == "__main__":
    ### parse argument ###
    parser=argparse.ArgumentParser()
    parser.add_argument("-c", "--casename", type=str, required = True, help = "The target test case name in the config file")
    parser.add_argument("-l", "--config-locust", type=str, default="./config/config_locust.json", help = "Path to the config file (default ./config_locust.json)")
    parser.add_argument("-p", "--config-prom", type=str, default="./config/config_prom.json", help = "Path to the config file (default ./config_locust.json)")
    parser.add_argument("-f", "--result-filepath", type=str, default="./result/", help = "Path to the result directory (default ./result/)")
    args = parser.parse_args()

    ### run workload by locust ###
    print(f"Running test case '{args.casename}'...")
    start_time = datetime.now()
    run(args.config_locust, args.casename)
    end_time = datetime.now()
    print("\nDone")

    # ### gather resource metric from prometheus ###
    prom_client_dict = create_prom_client_dict(args.config_prom)
    df_metrics = pd.DataFrame(columns = ["cpu", "memory"])
    df_metrics.index.name = "hostname"
    for url in prom_client_dict:
        # cpu
        cpu = cpu_avg_utilization(prom_client_dict[url], start_time, end_time)
        for hostname in cpu:
            df_metrics.loc[hostname.split(':')[0], "cpu"] = cpu[hostname]

        # memory
        memory = memory_avg_utilization(prom_client_dict[url], start_time, end_time)
        for hostname in memory:
            df_metrics.loc[hostname.split(':')[0], "memory"] = memory[hostname]


    df_metrics.reset_index(inplace = True)
    print(df_metrics)
    df_metrics.to_csv(f"{args.casename}_metrics.csv", index = False)