from locust import HttpUser, TaskSet, task, tag

### Task ###
class ExampleBenchmark(TaskSet):
    @task
    def nodeinfo(self):
        self.client.get("/function/nodeinfo")

class MicroBenchmark(TaskSet):
    @tag('memory', 'cpu')
    @task
    def matrix_multiplication(self):
        self.client.get("/function/matrix-multiplication")

    @tag('cpu')
    @task
    def floating_point_operation_sine(self):
        self.client.get("/function/floating-point-operation-sine")

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


class CPUUser(HttpUser):
    tasks = [MicroBenchmark.floating_point_operation_sine]


class MemoryUser(HttpUser):
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