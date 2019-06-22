from django.db import models
from common.util import random_str32


class Worker(models.Model):
    uid = models.CharField(primary_key=True, max_length=32)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    login_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_worker_uid():
        uid = "wuid_"
        uid += random_str32()[-27:]
        return uid

    def verify(self, password):
        return self.password == password
        # return hasher.verify(password, self.hash_password)
