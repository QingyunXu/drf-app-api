from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


from core import models
from core.models import PlayList
from song.serializers.playlistSerializers import PlayListSerializer

from .test_identity_api import crate_example_user

# create playlist URL
PLAYLIST_URL = reverse('song:playlist-list')


class PlayListStr(TestCase):
    """Test the playlist string representation"""

    def test_playlist_str(self):
        """Test the playlist string representation"""
        pl = models.PlayList.objects.create(
            user=crate_example_user(),
            name='Focus'
        )
        self.assertEqual(str(pl), pl.name)


###########################################################
# Test public authentication                              #
###########################################################


class PublicPlayListApiTests(TestCase):
    """Test the publicly available playlist API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving playlist"""
        response = self.client.get(PLAYLIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


###########################################################
# Test private authentication                             #
###########################################################


class PrivatePlayListApiTests(TestCase):
    """Test the authorized user playlist API"""

    def setUp(self):
        self.user = crate_example_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    ###########################################################
    # Test Get and Retrieve                                   #
    ###########################################################

    def test_retrieve_play_list(self):
        """Test retrieving playlist"""
        PlayList.objects.create(user=self.user, name='Focus')
        PlayList.objects.create(user=self.user, name='Running')

        response = self.client.get(PLAYLIST_URL)

        # playlist returns in the order of name,reverse
        pl = PlayList.objects.all().order_by('-name')
        serializer = PlayListSerializer(pl, many=True)
        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # api response data should be same as serializer returns
        self.assertEqual(response.data, serializer.data)

    def test_playlist_limited_to_user(self):
        """Test that playlist returned are for the authenticated user"""
        user2 = crate_example_user(
            email='user@emailaddress.com', password='Test.1234')
        PlayList.objects.create(user=user2, name='Study')
        # pl belongs to self user
        pl = PlayList.objects.create(user=self.user, name='Soothing')

        response = self.client.get(PLAYLIST_URL)

        # status code, should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self user only hafe 1 pl
        self.assertEqual(len(response.data), 1)
        # the return name should be same
        self.assertEqual(response.data[0]['name'], pl.name)

    ###########################################################
    # Test Write methods                                      #
    ###########################################################

    def test_create_play_list_exists(self):
        """Test creating a new playlist"""
        payload = {'name': 'Soothing'}
        self.client.post(PLAYLIST_URL, payload)
        # check the payload exists in DB
        exists = PlayList.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_play_list_invalid(self):
        """Test creating a new playlist with invalid name"""
        payload = {'name': ''}
        res = self.client.post(PLAYLIST_URL, payload)
        # status code should be 400 bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
