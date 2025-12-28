from django.test import RequestFactory
from django.contrib.auth import get_user_model
from app_tickets.views import TicketUpdateView, TicketDeleteView
from app_tickets.models import Ticket

def test_permissions():
    """Testa se as permissões de edição/exclusão de app_tickets estão corretas."""
    User = get_user_model()
    # Create test users
    creator, _ = User.objects.get_or_create(email='creator@test.com')
    other, _ = User.objects.get_or_create(email='other@test.com')
    staff, _ = User.objects.get_or_create(email='staff@test.com', is_staff=True)

    # Mock Ticket
    class MockTicket:
        requester = creator
        pk = 1

    view_update = TicketUpdateView()
    view_update.get_object = lambda: MockTicket()
    
    view_delete = TicketDeleteView()
    view_delete.get_object = lambda: MockTicket()

    # Test Creator Access (Should be True)
    view_update.request = type('Request', (), {'user': creator})()
    print(f"Creator can edit: {view_update.test_func()}")
    
    view_delete.request = type('Request', (), {'user': creator})()
    print(f"Creator can delete: {view_delete.test_func()}")

    # Test Other User Access (Should be False)
    view_update.request = type('Request', (), {'user': other})()
    print(f"Other can edit: {view_update.test_func()}")

    # Test Staff Access (Should be True)
    view_update.request = type('Request', (), {'user': staff})()
    print(f"Staff can edit: {view_update.test_func()}")

if __name__ == "__main__":
    test_permissions()
