from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from app_tickets.models import Ticket
from app_management.models import Project
from django.contrib.auth import get_user_model

class ReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'app_reports/reports.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filters
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        project_id = self.request.GET.get('project')

        queryset = Ticket.objects.all()

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        # Overview Stats
        context['total_tickets'] = queryset.count()
        context['open_tickets'] = queryset.filter(status=Ticket.STATUS_OPEN).count()
        context['closed_tickets'] = queryset.filter(status=Ticket.STATUS_DONE).count()

        # By Status
        context['tickets_by_status'] = queryset.values('status').annotate(count=Count('id')).order_by('-count')

        # By Project
        context['tickets_by_project'] = queryset.values('project__name').annotate(count=Count('id')).order_by('-count')

        # By Assignee
        context['tickets_by_assignee'] = queryset.values('assignee__email').annotate(count=Count('id')).order_by('-count')

        # Evolution (Last 12 months)
        last_year = timezone.now() - timedelta(days=365)
        context['tickets_evolution'] = Ticket.objects.filter(created_at__gte=last_year).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(count=Count('id')).order_by('month')

        # Context for filters
        context['projects'] = Project.objects.all()
        if project_id:
            try:
                context['selected_project_id'] = int(project_id)
            except ValueError:
                context['selected_project_id'] = None
        
        return context
