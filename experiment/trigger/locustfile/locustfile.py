from locust import HttpUser, TaskSet, task, tag
import uuid

user_request_target =500
user_request_count_map = {}


class MicroBenchmark(TaskSet):
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

    @task            
    def resize_image(self):
        image_url =  "http://10.202.0.99:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2V4cGVyaW1lbnQvd2F0ZXJkcm9wLmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTE2R1hEU080OTE1QjVGRk40Qk8xJTJGMjAyNDA4MjUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwODI1VDExNDUxN1omWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXhOa2RZUkZOUE5Ea3hOVUkxUmtaT05FSlBNU0lzSW1WNGNDSTZNVGN5TkRZeU9UVXhNU3dpY0dGeVpXNTBJam9pWVdSdGFXNGlmUS5BckVoNnhEczJZOWNMQldMdFhlOUZ0T0lGS2dpOHNNTGZxY043dy04WUp6RVBRMTFNTWhUeDFIelplaEFGc0RXUmlMLU82N25lVzljUVQ1ZW8teEtLUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPW51bGwmWC1BbXotU2lnbmF0dXJlPTlkMDMxN2U1MzNiM2U2MzZkNGM3MWFhYWY5NDM2Mjc3NmE0YzA1M2YzZDQyMjdjOTU2ZTViZWQ1ZWE4Y2M4NWE"
        resp = self.client.post("/function/resize-image", data = image_url)
        # to control total invocation
        global user_request_count_map
        global user_request_target
        user_request_count_map[self.user_id] += 1
        if user_request_count_map[self.user_id] == user_request_target:
            self._state = "stopping"
            del user_request_count_map[self.user_id]



### User ###
class IdleUser(HttpUser):
    tasks = []

class CPUUser(HttpUser):
    def on_start(self):
        global user_request_count_map
        self.user_id = str(uuid.uuid4())
        user_request_count_map[self.user_id] = 0
    def on_stop(self):
        global user_request_count_map
        if len(user_request_count_map) == 0:
            self.environment.runner.quit()

    # tasks = [MicroBenchmark.floating_point_operation_sine]
    tasks = [MicroBenchmark.resize_image]