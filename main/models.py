from django.db import models

class Facebook(models.Model):
    access_token = models.CharField(max_length=500)
    user_id = models.IntegerField()
    login_status = models.BooleanField()
    name = models.CharField(max_length=500)

class Messages(models.Model):
    message = models.TextField(null=True)
    Location = models.CharField(max_length=500)
