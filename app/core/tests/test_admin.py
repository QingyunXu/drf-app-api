from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Setup tasks need to be done before tests below"""
        self.client = Client()
        # create a super user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com', password='Text.1234')
        # user client helper function to login
        self.client.force_login(self.admin_user)
        # create a general user
        self.user = get_user_model().objects.create_user(
            email='test@test.com', password='Text.1234', name='My name')

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # generate a url for user list page
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        # check the response contain certain item
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_page_change(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        # check the page runs ok
        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        # check the create page works
        self.assertEqual(response.status_code, 200)
