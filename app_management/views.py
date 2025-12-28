from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Topic
from .forms import ProjectForm, TopicForm

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin que exige status de staff para acesso."""
    def test_func(self):
        return self.request.user.is_staff

# Team Views
from django.contrib.auth import get_user_model
from app_accounts.forms import CustomUserCreationForm

# Developer Views (Users)
class DeveloperListView(StaffRequiredMixin, ListView):
    """Lista todos os desenvolvedores (usuários)."""
    model = get_user_model()
    template_name = 'app_core/developer_list.html'
    context_object_name = 'developers'

class DeveloperCreateView(StaffRequiredMixin, CreateView):
    """Cria um novo desenvolvedor."""
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'app_core/developer_form.html'
    success_url = reverse_lazy('developer-list')

# Project Views
class ProjectListView(StaffRequiredMixin, ListView):
    """Lista todos os projetos."""
    model = Project
    template_name = 'app_core/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(StaffRequiredMixin, DetailView):
    """Detalhes do projeto."""
    model = Project
    template_name = 'app_core/project_detail.html'
    context_object_name = 'project'


class ProjectCreateView(StaffRequiredMixin, CreateView):
    """Cria um novo projeto."""
    model = Project
    form_class = ProjectForm
    template_name = 'app_core/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    """Atualiza um projeto existente."""
    model = Project
    form_class = ProjectForm
    template_name = 'app_core/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    """Remove um projeto."""
    model = Project
    template_name = 'app_core/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')

# Topic Views
class TopicListView(StaffRequiredMixin, ListView):
    """Lista todos os tópicos."""
    model = Topic
    template_name = 'app_core/topic_list.html'
    context_object_name = 'topics'

class TopicCreateView(StaffRequiredMixin, CreateView):
    """Cria um novo tópico."""
    model = Topic
    form_class = TopicForm
    template_name = 'app_core/topic_form.html'
    success_url = reverse_lazy('topic-list')

class TopicUpdateView(StaffRequiredMixin, UpdateView):
    """Atualiza um tópico existente."""
    model = Topic
    form_class = TopicForm
    template_name = 'app_core/topic_form.html'
    success_url = reverse_lazy('topic-list')

class TopicDeleteView(StaffRequiredMixin, DeleteView):
    """Remove um tópico."""
    model = Topic
    template_name = 'app_core/topic_confirm_delete.html'
    success_url = reverse_lazy('topic-list')


from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from app_tickets.models import Ticket

class DashboardView(LoginRequiredMixin, TemplateView):
    """View do painel principal (Dashboard)."""
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        """Retorna dados estatísticos para o dashboard."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_staff:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(requester=user)

        context['tickets_open'] = queryset.filter(status=Ticket.STATUS_OPEN).count()
        # Including ACCEPTED in "In Progress" for dashboard overview if desired, or keep separate. 
        # Design shows "Em Andamento". Let's group ACCEPTED and IN_PROGRESS as active work.
        context['tickets_in_progress'] = queryset.filter(status__in=[Ticket.STATUS_IN_PROGRESS, Ticket.STATUS_ACCEPTED]).count()
        context['tickets_done'] = queryset.filter(status=Ticket.STATUS_DONE).count()
        context['tickets_blocked'] = queryset.filter(status=Ticket.STATUS_BLOCKED).count()
        
        context['recent_tickets'] = queryset.order_by('-created_at')[:5]
            
        return context

