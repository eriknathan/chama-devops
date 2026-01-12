from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('new/', views.TopicSelectView.as_view(), name='ticket-new'),




    path('new/topic/<int:pk>/', views.DynamicTicketCreateView.as_view(), name='ticket-form-dynamic'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket-delete'),
    path('<int:pk>/action/<str:action>/', views.ticket_action_view, name='ticket-action'),
    path('<int:pk>/pdf/', views.TicketPDFView.as_view(), name='ticket-pdf'),
]
