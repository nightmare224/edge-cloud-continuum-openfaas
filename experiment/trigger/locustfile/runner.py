import gevent
import json
from time import sleep
from locust.env import Environment
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter, print_stats_json
from .locustfile import *

def user_factory(name, base_class, attrs):
    return type(name, (base_class, ), attrs)

def load_case_config(config_filename, casename):
    with open(config_filename, 'r') as f:
        data = json.load(f)
    if casename not in data:
        raise Exception(f"The case '{casename}' can not be found in configuration file.")
    
    return data[casename]

def run(config_filename, casename):
    config = load_case_config(config_filename, casename)
    users = []
    for i, host in enumerate(config["user_host"]):
        user = user_factory(f"user{i}", eval(f"{config['user_type']}"), {"host": host})
        users.append(user)


    # no user, no task, just idle and return    
    if len(users) == 0:
        config["runtime_second"]
        sleep(config["runtime_second"])
        return

    # setup Environment and Runner
    env = Environment(user_classes = users)#, shape_class = StepLoadShape())
    runner = env.create_local_runner()

    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))

    # start a greenlet that save current stats to history and output to csv file
    gevent.spawn(stats_history, env.runner)

    # Writing all the stats to a CSV file
    # csv_writer = StatsCSVFileWriter(env, [], config["result_file_basename"], False)
    csv_writer = StatsCSVFileWriter(env, [], casename, False)
    gevent.spawn(csv_writer.stats_writer)

    # start the test
    runner.start(user_count = int(config["user_count"]), spawn_rate=config["spawn_rate"])
    # runner.start(user_count = int(config["user_count"]))

    # in 10 seconds stop the runner
    gevent.spawn_later(int(config["runtime_second"]), runner.quit)

    # wait for the greenlets
    env.runner.greenlet.join()



