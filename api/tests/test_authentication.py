from django.test import TestCase


class RegistrationTestCase(TestCase):

    valid_user_data = {
            'username': 'testUser',
            'email': 'testemail@email.com',
            'password': 'testpassword'
            }

    def test_registration_with_valid_params(self):
        response = self.client.post('/api/v1/users/', self.valid_user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'testUser')

    def test_registration_with_already_invalid_email(self):
        invalid_data = dict(self.valid_user_data)
        invalid_data['email'] = "fakeemail"
        first_response = self.client.post('/api/v1/users/',
                                          self.valid_user_data)
        duplicate_response = self.client.post('/api/v1/users/',
                                              self.valid_user_data)

        invalid_response = self.client.post('/api/v1/users/', invalid_data)
        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertIn("user with this email already exists",
                      duplicate_response.data['email'][0])
        self.assertIn("Enter a valid email address",
                      invalid_response.data['email'][0])

    def test_registration_with_invalid_username(self):
        user_data = dict(self.valid_user_data)
        user_data['username'] = ''

        response = self.client.post('/api/v1/users', user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("This field may not be blank.",
                      response.data['username'][0])

    def test_registration_with_invalid_password(self):
        user_data = dict(self.valid_user_data)
        user_data['password'] = '12345'

        response = self.client.post('/api/v1/users', user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Ensure this field has at least 8 characters.",
                      response.data['password'][0])


class LoginTestCase(TestCase):

    user_data = {
        'username': 'testUser',
        'email': 'testloginemail@email.com',
        'password': 'testpassword'
    }

    def test_login_with_correct_credentials(self):
        self.client.post('/api/v1/users/', self.user_data)
        response = self.client.post('/api/v1/users/login/', self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_with_incorrect_credentials(self):
        err_login_data = {
                'email': 'testloginemail@email.com',
                'password': 'faketestpassword'
        }

        response = self.client.post('/api/v1/users/login/', err_login_data)
        self.assertEqual(response.status_code, 400)
