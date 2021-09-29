import uuid
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.CharField(primary_key=True, unique=True, default=uuid.uuid4, max_length=50)
    name = models.CharField(max_length=500)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    image = models.CharField(max_length=500, default='/main/profiles/default.jpg')
    access_token = models.CharField(max_length=500)
    password = models.CharField(max_length=500)  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    objects = UserManager()
    def __str__(self):
        return self.name

class Messages(models.Model):
    message = models.TextField(null=True, blank=True)
    Location = models.CharField(max_length=500, null=True, blank=True)
    models.ForeignKey(User, on_delete=models.CASCADE)

