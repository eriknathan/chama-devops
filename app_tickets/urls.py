from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('new/', views.TopicSelectView.as_view(), name='ticket-new'),
    path('new/repository/', views.RepositoryFormView.as_view(), name='ticket-form-repository'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/edit/', views.TicketUpdateView.as_view(), name='ticket-edit'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket-delete'),
    path('<int:pk>/action/<str:action>/', views.ticket_action_view, name='ticket-action'),
    path('<int:pk>/pdf/', views.TicketPDFView.as_view(), name='ticket-pdf'),
]
