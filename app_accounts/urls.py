from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, CustomLoginView, ProfileView, UserListView, UserDetailView, UserUpdateView, AdminUserPasswordChangeView, UserCreateView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # User Management (Staff Only)
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/add/', UserCreateView.as_view(), name='user-add'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('users/<int:pk>/password/', AdminUserPasswordChangeView.as_view(), name='admin-user-password'),
]
