import argparse
import json
import os
import shutil
import glob
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

    ### gather resource metric from prometheus ###
    prom_client_dict = create_prom_client_dict(args.config_prom)
    metrics_dict = {'cpu':{}, 'memory':{}}
    for url in prom_client_dict:
        # cpu
        cpu = cpu_avg_utilization(prom_client_dict[url], start_time, end_time)
        metrics_dict['cpu'].update(cpu)
        # memory
        memory = memory_avg_utilization(prom_client_dict[url], start_time, end_time)
        metrics_dict['memory'].update(memory)
    # Writing dictionary to JSON file
    with open(f"{args.casename}_resource_metric.json", 'w') as json_file:
        json.dump(metrics_dict, json_file)

    ### move result all to result directory ###
    # Ensure the destination directory exists
    if not os.path.exists(args.result_filepath):
        os.makedirs(args.result_filepath)
    # Use glob to find files matching the pattern
    files_to_move = glob.glob(args.casename)
    for file_path in files_to_move:
        shutil.move(file_path, args.result_filepath)