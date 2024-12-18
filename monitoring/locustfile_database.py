# Usage: locust -f locustfile.py --headless --users 10 --spawn-rate 1 -H http://localhost:8000
from locust import HttpUser, task, between
import random
import string


class DatabaseUser(HttpUser):
    wait_time = between(1, 5)

    @task(5)
    def random_sleep(self):
        self.client.get("/select_user/1", name="/select_user/1")

    @task(2)
    def random_sleep(self):
        self.client.get("/select_user/2", name="/select_user/2")

    @task(10)
    def random_sleep(self):
        self.client.get("/test", name="/test")
    
    @task(7)
    def random_sleep(self):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{username}@gmail.com"
        self.client.get(f"/insert_user/{username}/{email}", name="/insert_user")