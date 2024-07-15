from locust import HttpUser, TaskSet, task, tag
import uuid

user_request_target = 500
user_request_count_map = {}

### Task ###
class ExampleBenchmark(TaskSet):
    @task
    def nodeinfo(self):
        self.client.get("/function/nodeinfo")

        # to control total invocation
        global user_request_count_map
        global user_request_target
        user_request_count_map[self.user_id] += 1
        if user_request_count_map[self.user_id] == user_request_target:
            self._state = "stopping"
            del user_request_count_map[self.user_id]

class MicroBenchmark(TaskSet):
    @tag('memory', 'cpu')
    @task
    def matrix_multiplication(self):
        self.client.get("/function/matrix-multiplication")

    @tag('cpu')
    @task
    def floating_point_operation_sine(self):
        self.client.get("/function/floating-point-operation-sine")

        # to control total invocation
        global user_request_count_map
        global user_request_target
        user_request_count_map[self.user_id] += 1
        if user_request_count_map[self.user_id] == user_request_target:
            self._state = "stopping"
            del user_request_count_map[self.user_id]

    @tag('memory')
    @task
    def sorter(self):
        self.client.get("/function/sorter")

# class AplicationLevelBenchmark(TaskSet):
#     @task
#     def hello_world(self):
#         self.client.get("/function/env")

### User ###
class IdleUser(HttpUser):
    tasks = []

class ExampleUser(HttpUser):
    def on_start(self):
        global user_request_count_map
        self.user_id = str(uuid.uuid4())
        user_request_count_map[self.user_id] = 0
    def on_stop(self):
        global user_request_count_map
        if len(user_request_count_map) == 0:
            self.environment.runner.quit()
    
    tasks = [ExampleBenchmark.nodeinfo]

class CPUUser(HttpUser):
    def on_start(self):
        global user_request_count_map
        self.user_id = str(uuid.uuid4())
        user_request_count_map[self.user_id] = 0
    def on_stop(self):
        global user_request_count_map
        if len(user_request_count_map) == 0:
            self.environment.runner.quit()

    tasks = [MicroBenchmark.floating_point_operation_sine]


class MemoryUser(HttpUser):
    def on_start(self):
        global user_request_count_map
        self.user_id = str(uuid.uuid4())
        user_request_count_map[self.user_id] = 0
    def on_stop(self):
        global user_request_count_map
        if len(user_request_count_map) == 0:
            self.environment.runner.quit()
            
    tasks = [MicroBenchmark.floating_point_operation_sine]



# class StepLoadShape(LoadTestShape):
#     """
#     A step load shape

#     Keyword arguments:

#         step_time -- Time between steps
#         step_load -- User increase amount at each step
#         spawn_rate -- Users to stop/start per second at every step
#         time_limit -- Time limit in seconds
#     """
#     step_time = 10
#     step_load = 0
#     spawn_rate = 1
#     time_limit = 60
#     def tick(self):
#         run_time = self.get_run_time()
#         if run_time > self.time_limit:
#             return None
#         current_step = math.floor(run_time / self.step_time) + 1
#         return (current_step * self.step_load, self.spawn_rate)