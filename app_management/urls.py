from django.urls import path
from . import views

urlpatterns = [
    # Developers (Unified with Users, see app_accounts/urls.py)
    # path('developers/', ...),


    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/add/', views.ProjectCreateView.as_view(), name='project-add'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),

    # Topics
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/add/', views.TopicCreateView.as_view(), name='topic-add'),
    path('topics/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic-edit'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic-delete'),
]
