from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Role

# May need to run ALTER USER <username> CREATEDB; in psql to allow the user to create databases
class UserTests(APITestCase):
    def setUp(self):
        Role.objects.create(role_name="Test Role")
        roleC = Role.objects.create(role_name="Test Role 3")
        User.objects.create(name="Test User 3", email="test3@example.com", password="test12345", role_id=roleC, subcomm="Subcomm3")

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        data = {
            "name": "Test User",
            "password": "verysecurepassword",
            "email": "test@example.com",
            "subcomm": "Test Subcomm",
            "role_id": 1
        }

        url = reverse('user-list-create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2) # 1 user created in this test case + 1 from setUp
        self.assertIn('Test User', [user.name for user in User.objects.all()])

    def test_view_all_users(self):
        """
        Ensure we can view all users.
        """
        roleB = Role.objects.create(role_name="Test Role 2")
        User.objects.create(name="Test User 2", email="test2@example.com", password="test12345", role_id=roleB, subcomm="Subcomm2")

        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # 1 user created in this test case + 1 from setUp

    def test_view_user_by_id(self):
        """
        Ensure we can view a single user by ID.
        """
        user = User.objects.get(email="test3@example.com") # test3user created in setUp
        url = reverse('user-detail', args=[user.user_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
