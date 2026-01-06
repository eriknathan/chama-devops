from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from app_management.models import Project, Topic
from ..models import Ticket, Comment
from ..forms import CommentForm

class TicketListView(LoginRequiredMixin, ListView):
    """Lista tickets com filtros."""
    model = Ticket
    template_name = 'app_tickets/ticket_list.html'
    context_object_name = 'tickets'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtra tickets baseado em status, projeto, responsável e busca."""
        queryset = super().get_queryset()
        
        # Base filter: Staff sees all, others see only their requests
        if not self.request.user.is_staff:
            queryset = queryset.filter(requester=self.request.user)
            
        # Search (Title or Description)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
            
        # Filter by Project
        project_id = self.request.GET.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
            
        # Filter by Status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by Assignee (Developer)
        assignee_id = self.request.GET.get('assignee')
        if assignee_id:
            queryset = queryset.filter(assignee_id=assignee_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['developers'] = get_user_model().objects.all()
        context['status_choices'] = Ticket.STATUS_CHOICES
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    """Exibe detalhes de um ticket."""
    model = Ticket
    template_name = 'app_tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        # Allow user to see only their tickets, staff sees all
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(requester=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """Processa a criação de comentários."""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = self.object
            comment.author = request.user
            comment.save()
            return redirect('ticket-detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(comment_form=form))


class TopicSelectView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Exibe lista de tópicos para seleção antes de criar ticket."""
    model = None
    template_name = 'app_tickets/topic_select.html'
    context_object_name = 'topics'

    def test_func(self):
        # Admins (staff) cannot create tickets, only common users
        return not self.request.user.is_staff

    def get_queryset(self):
        return Topic.objects.all()
