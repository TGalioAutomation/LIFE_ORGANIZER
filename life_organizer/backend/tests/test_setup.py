import pytest
from django.test import TestCase
from django.contrib.auth.models import User

class SetupTest(TestCase):
    def test_django_setup(self):
        """Test that Django is properly configured"""
        self.assertTrue(True)
    
    def test_user_creation(self):
        """Test basic user creation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
