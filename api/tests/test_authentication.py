from django.test import TestCase


class RegistrationTestCase(TestCase):

    valid_user_data = {
            'username': 'testUser',
            'email': 'testemail@email.com',
            'password': 'testpassword'
            }

    def test_registration_with_valid_params(self):
        response = self.client.post('/users/', self.valid_user_data)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.data['username'], 'testUser')

    def test_registration_with_already_invalid_email(self):
        invalid_data = self.valid_user_data
        invalid_data['email'] = "fakeemail"
        first_response = self.client.post('/users/', self.valid_user_data)
        duplicate_response = self.client.post('/users/', self.valid_user_data)

        invalid_response = self.client.post('/users/', invalid_data)
        self.assertEqual(first_response.status, 200)
        self.assertEqual(duplicate_response.status, 400)
        self.assertIn("A User with this email already exists",
                      duplicate_response.data['non_field_errors'])
        self.assertIn("Invalid email",
                      invalid_response.data['non_field_errors'])

    def test_registration_with_invalid_username(self):
        user_data = self.valid_user_data
        user_data['username'] = ''

        response = self.client.post('/users', user_data)
        self.assertEqual(response.status, 400)
        self.assertIn("Invalid username", response.data['non_field_errors'])

    def test_registration_with_invalid_password(self):
        user_data = self.valid_user_data
        user_data['password'] = '12345'

        response = self.client.post('/users', user_data)
        self.assertEqual(response.status, 400)
        self.assertIn("Invalid password", response.data['non_field_errors'])


class LoginTestCase(TestCase):
    def test_login_with_correct_credentials(self):
        login_data = {
                'email': "testloginemail@email.com",
                'password': 'testpassword'
        }
        response = self.client.post('/login/', login_data)
        self.assertEqual(response.status, 200)
        self.assertIn('token', response.data)

    def test_login_with_incorrect_credentials(self):
        err_login_data = {
                'email': 'testloginemail@email.com',
                'password': 'faketestpassword'
        }

        response = self.client.post('/login/', err_login_data)
        self.assertEqual(response.status, 401)
        self.assertIn('Authentication failed',
                      response.data['non_field_errors'])
