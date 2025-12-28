from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
# from app_management.views import HomeView  <-- HomeView is being removed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('app_accounts.urls')),
    path('management/', include('app_management.urls')),
    path('tickets/', include('app_tickets.urls')),
    path('reports/', include('app_reports.urls')),
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
