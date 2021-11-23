from django.contrib.auth import get_user_model
from django.test import TestCase


class UserTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@emailaddress.com'
        password = 'Test.1234'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_creating_user_with_no_email_or_password(self):
        email = 'test@emailaddress.com'
        password = 'Test.1234'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password=password)
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password=password)
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=email, password=None)
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=email, password='')
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password=None)
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='')

    def test_new_user_email_normalized(self):
        email = 'test@EMALADDRESS.com'
        password = 'Test.1234'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email.lower())

    def test_create_super_user(self):
        """Test creating a new user with an email is successful"""
        email = 'test@emailaddress.com'
        password = 'Test.1234'
        user = get_user_model().objects.create_superuser(
            email=email, password=password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
