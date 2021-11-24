from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# create user create URL
RETISTER_USER_URL = reverse('identity:register')
TOKEN_URL = reverse('identity:login')
PROFILE_URL = reverse('identity:profile')


def crate_example_user(**params):
    """create example users for test"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Setup tasks need to be done before tests below"""

    def setup(self):
        self.client = APIClient()

    ###########################################################
    # Test create user                                        #
    ###########################################################

    def test_create_valid_user_success(self):
        """Test creating user with valid values"""
        payload = {
            'email': 'test@emailaddress.com',
            'password': 'Test.1234',
            'name': 'username'
        }
        response = self.client.post(RETISTER_USER_URL, payload)

        # test status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test the object is actually created
        user = get_user_model().objects.get(**response.data)
        # test the password is correct
        self.assertTrue(user.check_password(payload['password']))
        # test the password is not returned in request data
        self.assertNotIn('password', response.data)

    def test_create_existing_user_success(self):
        """Test creating a user that email address exists"""
        payload = {
            'email': 'test@emailaddress.com',
            'password': 'Test.1234',
            'name': 'username'
        }
        # create example user
        crate_example_user(**payload)

        # post create request
        response = self.client.post(RETISTER_USER_URL, payload)

        # test status code,should return bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_format_invalid(self):
        """Test password with invalid format"""
        payload = {
            'email': 'test@emailaddress.com',
            'password': '123',
            'name': 'username'
        }
        response = self.client.post(RETISTER_USER_URL, payload)

        # test status code, should return bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # user should not be created
        self.assertFalse(
            get_user_model().objects.filter(email=payload['email']).exists()
        )

    ###########################################################
    # Test create token                                       #
    ###########################################################

    def test_create_token(self):
        """Test a token is created for a valid user"""
        payload = {
            'email': 'test@emailaddress.com',
            'password': 'Test.1234',
            'name': 'username'
        }
        # create example user
        crate_example_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        # a token value shoud be returned in response data
        self.assertIn('token', response.data)
        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials(self):
        """Test that token is not created if credentials are invalid"""
        crate_example_user(email='test@emailaddress.com', password='Test.1234')
        payload = {
            'email': 'test@emailaddress.com',
            'password': 'wrong_password'
        }
        response = self.client.post(TOKEN_URL, payload)

        # a token value shoudn't be returned in response data
        self.assertNotIn('token', response.data)
        # status code, should be 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test that token is not created if user doesn't exist"""
        payload = {
            'email': 'user@emailaddress.com',
            'password': 'wrong_password'
        }
        response = self.client.post(TOKEN_URL, payload)

        # a token value shoudn't be returned in response data
        self.assertNotIn('token', response.data)
        # status code, should be 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': '', 'password': ''}
        response = self.client.post(TOKEN_URL, payload)

        # a token value shoudn't be returned in response data
        self.assertNotIn('token', response.data)
        # status code, should be 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticationUserApi(TestCase):
    """Test API requests that require authentication"""

    ###########################################################
    # Test user permissions                                   #
    ###########################################################

    def setUp(self):
        self.user = crate_example_user(
            email='test@emailaddress.com',
            password='Test.1234',
            name='username'
        )
        self.client = APIClient()
        # make auth request
        self.client.force_authenticate(user=self.user)

    def test_retrieve_success(self):
        """Test retrieving profile for logged in used"""
        response = self.client.get(PROFILE_URL)

        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user details should be returned
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed"""
        response = self.client.post(PROFILE_URL, {})
        # status code, should be 405 not alowed
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'new_password'}
        response = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()

        # user details should be equal
        self.assertEqual(response.data.get('name'), payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
