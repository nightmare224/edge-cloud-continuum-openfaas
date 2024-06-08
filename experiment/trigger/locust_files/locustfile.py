from locust import HttpUser, TaskSet, task, tag



class ExampleBenchmark(TaskSet):
    @task
    def env(self):
        self.client.get("/function/env")

class MicroBenchmark(TaskSet):
    @tag('memory', 'cpu')
    @task
    def matrix_multiplication(self):
        self.client.get("/function/matrix-multiplication")

    @task('cpu')
    def floating_point_operation_sine(self):
        self.client.get("/function/floating-point-operation-sine")

    @task('memory')
    def sorter(self):
        self.client.get("/function/sorter")

    @task('io')
    def dd_cmd(self):
        self.client.get("/function/dd-cmd")

class AplicationLevelBenchmark(TaskSet):
    @task
    def hello_world(self):
        self.client.get("/function/env")

class ExampleUser(HttpUser):
    tasks = [ExampleBenchmark]

class EdgeUser(HttpUser):
    tasks = [MicroBenchmark]

