from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TicketPermissionTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.common_user = User.objects.create_user(
            email='user@example.com', 
            password='password123'
        )
        self.staff_user = User.objects.create_user(
            email='admin@example.com', 
            password='password123', 
            is_staff=True
        )
        self.url = reverse('ticket-add')

    def test_common_user_can_access_create_view(self):
        """Users without staff status should be able to access the create view."""
        self.client.force_login(self.common_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_staff_user_cannot_access_create_view(self):
        """Staff users should be denied access (403 Forbidden)."""
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
