from locust import HttpUser, TaskSet, task, tag

# Task
class ExampleBenchmark(TaskSet):
    @task
    def env(self):
        self.client.get("/function/env")

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

    @tag('io')
    @task
    def dd_cmd(self):
        self.client.get("/function/dd-cmd")

class AplicationLevelBenchmark(TaskSet):
    @task
    def hello_world(self):
        self.client.get("/function/env")


# User
class ExampleUser(HttpUser):
    tasks = [ExampleBenchmark]

class EdgeUser(HttpUser):
    tasks = [MicroBenchmark]

