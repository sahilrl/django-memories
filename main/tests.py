from django.test import TestCase
from .models import User

class CreateUserTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='test@gmail.com',
                                                         password='woofer')
        print(user)