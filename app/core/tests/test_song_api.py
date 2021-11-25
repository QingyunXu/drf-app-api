from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Song

# create playlist URL
SONG_URL = reverse('song:song-list')


def detail_url(id):
    return reverse('song:song-list', args=[id])


def sample_song(**params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample song',
        'length': 5.00,
        'release': '1990-12-01 00:00:00'
    }
    defaults.update(params)

    return Song.objects.create(**defaults)


class PublicSongApiTests(TestCase):
    """Test unauthenticated is required"""

    def setUp(self):
        self.client = APIClient()

    def test_write_auth_required(self):
        response = self.client.post(SONG_URL)
        # Shsould return unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_unauth_required(self):
        response = self.client.get(SONG_URL)
        # should return success
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated api access"""

    def SetUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            email='user@emailaddress.com', password='Test.1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.superuser)
