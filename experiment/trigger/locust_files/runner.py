import gevent
import json
import argparse
import pprint
from locust.env import Environment
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter
import locustfile

def user_factory(name, base_class, attrs):
    return type(name, (base_class, ), attrs)

def load_case_config(config_filename, casename, ):
    with open(config_filename, 'r') as f:
        data = json.load(f)
    if casename not in data:
        raise Exception(f"The case '{casename}' can not be found in configuration file.")
    
    return data[casename]

def run(config):
    users = []
    for i, host in enumerate(config["user_host"]):
        user = user_factory(f"user{i}", eval(f"locustfile.{config['user_type']}"), {"host": host})
        users.append(user)

    # setup Environment and Runner
    env = Environment(user_classes = users)
    runner = env.create_local_runner()

    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))

    # start a greenlet that save current stats to history and output to csv file
    gevent.spawn(stats_history, env.runner)

    # Writing all the stats to a CSV file
    csv_writer = StatsCSVFileWriter(env, [], config["result_file_basename"], False)
    gevent.spawn(csv_writer.stats_writer)

    # start the test
    runner.start(user_count = int(config["user_count"])/len(users), spawn_rate=1)

    # in 10 seconds stop the runner
    gevent.spawn_later(int(config["runtime_second"]), runner.quit)

    # wait for the greenlets
    env.runner.greenlet.join()

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-c", "--configfile", type=str, default="./config.json", help = "Path to the config file (default ./config.json)")
    parser.add_argument("-n", "--casename", type=str, required = True, help = "The target test case name in the config file")
    args = parser.parse_args()

    config = load_case_config(args.configfile, args.casename)
    print(f"Test case '{args.casename}' config:\n")
    pprint.pp(config)
    print("\nRunning....")
    run(config)
    print("\nDone")


