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
        try:
            user = self.get(email=email)
            print(user.email)
        except User.DoesNotExist:
            user = self.model(
                email=self.normalize_email(email),
                **extra_fields
            )
            
            user.set_password(password)
            user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    # def create_superuser(self, email, password=None):
    #     """
    #     Creates and saves a superuser with the given email, date of
    #     birth and password.
    #     """
    #     user = self.create_user(
    #         email,
    #         password=password,
    #     )
    #     user.is_admin = True
    #     user.is_staff = True
    #     user.save(using=self._db)
    #     return user




class User(AbstractBaseUser):
    user_id = models.CharField(primary_key=True, unique=True, default=uuid.uuid4, max_length=50)
    name = models.CharField(max_length=500)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    image = models.CharField(max_length=500, default='/main/profiles/default.jpg')
    access_token = models.CharField(max_length=500)
    password = models.CharField(max_length=500, null=True, blank=True) 

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()
    def __str__(self):
        return self.name

class Messages(models.Model):
    message = models.TextField(null=True, blank=True)
    Location = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

