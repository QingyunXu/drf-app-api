from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core.models import Singer


# create playlist URL
SINGER_URL = reverse('song:singer-list')


class SingerStr(TestCase):
    """Test the playlist string representation"""

    def setUp(self):
        Singer.objects.create(name='Singer name')

    def test_singer_str(self):
        """Test the singer string representation"""
        singer = Singer.objects.create(name='Singer-name')
        self.assertEqual(str(singer), singer.name)


class PublicSingerApiTests(TestCase):
    ###########################################################
    # Test public list and reterive                           #
    ###########################################################
    def setUp(self):
        Singer.objects.create(name='Singer name')

    def test_singer_list_by_no_admin(self):
        self.superuser = None
        response = self.client.get(SINGER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_singer_by_no_admin(self):
        self.superuser = None
        # set select signer by id 1
        response = self.client.get(SINGER_URL, {'assigned_only': 1})
        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # the return name should be same
        self.assertEqual(response.data[0]['name'], 'Singer name')


class PrivateSingerApiTests(TestCase):
    ###########################################################
    # Test Write singer                                       #
    ###########################################################

    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            email='user@emailaddress.com', password='Test.1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.superuser)
        Singer.objects.create(name='Singer one')
        Singer.objects.create(name='Singer two')
        Singer.objects.create(name='Singer three')

    ###########################################################
    # Test create singer                                      #
    ###########################################################

    def test_admin_create_singer(self):
        response = self.client.post(SINGER_URL, {'name': 'Singer four'})
        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # the return name should be same
        print(response.data)
        self.assertEqual(response.data.get('name'), 'Singer four')

    def test_create_singer_invalid(self):
        response = self.client.post(SINGER_URL, {'name': ''})
        # status code should be 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_create_singer_false(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(SINGER_URL, {'name': 'Singer four'})
        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user_create_singer_false(self):
        user = get_user_model().objects.create_user(
            email='user@email.com', password='Test.1234'
        )
        self.client.force_authenticate(user=user)
        response = self.client.post(SINGER_URL, {'name': 'Singer four'})
        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)