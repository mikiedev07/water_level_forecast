from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import RegisterForm, LoginForm


class RegisterFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        self.invalid_data = {
            'username': '',
            'email': 'invalid_email',
            'password1': 'testpassword',
            'password2': 'different_password'
        }

    def test_valid_form(self):
        form = RegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = RegisterForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # Expecting 3 form errors

    def test_register_view(self):
        url = reverse('signup')  # Assuming you have a URL named 'register'
        response = self.client.post(url, data=self.valid_data)
        self.assertEqual(response.status_code, 200)  # Expecting successful registration


class LoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password1='testpassword')
        self.valid_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

    def test_valid_form(self):
        form = LoginForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = LoginForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Expecting 1 form error

    def test_login_view(self):
        url = reverse('signin')  # Assuming you have a URL named 'login'
        response = self.client.post(url, data=self.valid_data)
        self.assertEqual(response.status_code, 200)  # Expecting successful login
