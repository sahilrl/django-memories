from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.IntegerField()
    access_token = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    email = models.EmailField()
    image = models.CharField(max_length=500, default='/main/profiles/default.jpg')
    def __str__(self):
        return self.name

class Messages(models.Model):
    message = models.TextField(null=True, blank=True)
    Location = models.CharField(max_length=500, null=True, blank=True)
    models.ForeignKey(User, on_delete=models.CASCADE)

