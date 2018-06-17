from django.test import TestCase
from ..models import User

from rest_framework.test import APIClient


class BaseTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.setup_user = {'username': 'setup_user',
                           'email': 'setup_user@email.com',
                           'password': 'setup_password'}
        User.objects.create_user(**self.setup_user)
        self.login = self.client.post('/api/v1/users/login/', self.setup_user)
        self.setup_user_token = self.login.data['token']
        self.request_token = 'Bearer {}'.format(self.setup_user_token)

    def tearDown(self):
        User.objects.all().delete()
