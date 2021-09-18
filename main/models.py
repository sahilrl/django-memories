from django.db import models

class Facebook(models.Model):
    access_token = models.CharField(max_length=500)
    user_id = models.IntegerField()
    login_status = models.BooleanField(default=False)
    name = models.CharField(max_length=500)
    email = models.EmailField()
    def __str__(self):
        return self.name

class Messages(models.Model):
    message = models.TextField(null=True, blank=True)
    Location = models.CharField(max_length=500, null=True, blank=True)
    models.ForeignKey(Facebook, on_delete=models.CASCADE)

