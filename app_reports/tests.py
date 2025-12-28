from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from app_tickets.models import Ticket
from app_management.models import Project

class ReportsViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff_user = User.objects.create_user(
            email='admin@report.com', 
            password='password123', 
            is_staff=True
        )
        self.common_user = User.objects.create_user(
            email='user@report.com', 
            password='password123'
        )
        self.url = reverse('reports')
        
        # Setup data
        self.project = Project.objects.create(name="Test Project", description="Desc")
        Ticket.objects.create(
            title="Ticket 1", 
            description="Desc", 
            requester=self.common_user, 
            project=self.project,
            status=Ticket.STATUS_OPEN
        )

    def test_staff_can_access_reports(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_reports/reports.html')
        self.assertIn('total_tickets', response.context)
        self.assertEqual(response.context['total_tickets'], 1)

    def test_common_user_cannot_access_reports(self):
        self.client.force_login(self.common_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
