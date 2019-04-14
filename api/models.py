from django.db import models

class Worker(models.Model):
    uid = models.CharField(primary_key=True, max_length=32)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    login_time = models.DateTimeField(auto_now_add=True)
