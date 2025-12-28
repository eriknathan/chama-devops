from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('add/', views.TicketCreateView.as_view(), name='ticket-add'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/edit/', views.TicketUpdateView.as_view(), name='ticket-edit'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket-delete'),
    path('<int:pk>/action/<str:action>/', views.ticket_action_view, name='ticket-action'),
]
