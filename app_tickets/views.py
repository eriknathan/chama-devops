from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .models import Ticket, TicketAttachment, Comment
from .forms import TicketForm, CommentForm

from django.db.models import Q
from django.contrib.auth import get_user_model
from app_management.models import Project

class TicketListView(LoginRequiredMixin, ListView):
    """Lista app_tickets com filtros."""
    model = Ticket
    template_name = 'app_tickets/ticket_list.html'
    context_object_name = 'tickets'
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtra app_tickets baseado em status, projeto, responsável e busca."""
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
        # Allow user to see only their app_tickets, staff sees all
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


def ticket_action_view(request, pk, action):
    """Executa ações de mudança de estado em um ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if not request.user.is_staff:
        # Only staff can perform actions
        return redirect('ticket-detail', pk=pk)

    if action == 'take':
        ticket.assignee = request.user
        ticket.status = Ticket.STATUS_ACCEPTED
    elif action == 'start':
        ticket.status = Ticket.STATUS_IN_PROGRESS
    elif action == 'block':
        ticket.status = Ticket.STATUS_BLOCKED
    elif action == 'finish':
        ticket.status = Ticket.STATUS_DONE
    
    ticket._current_user = request.user
    ticket.save()
    return redirect('ticket-detail', pk=pk)

class TicketCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Cria um novo ticket."""
    model = Ticket
    form_class = TicketForm
    template_name = 'app_tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        # Admins (staff) cannot create tickets, only common users
        return not self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from app_management.models import Topic
        import json
        topics = Topic.objects.all()
        # Create a dictionary of {topic_id: template_text}
        topic_templates = {topic.pk: topic.template for topic in topics if topic.template}
        context['topic_templates'] = json.dumps(topic_templates)
        
        # Create a dictionary of {topic_id: form_fields_json}
        topic_forms = {topic.pk: topic.form_fields for topic in topics if topic.form_fields}
        context['topic_forms'] = json.dumps(topic_forms)
        
        return context

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.requester = self.request.user
        ticket._current_user = self.request.user
        ticket.save()
        
        # Handle attachment
        files = self.request.FILES.getlist('attachment')
        for file in files:
            TicketAttachment.objects.create(ticket=ticket, file=file)
            
        return redirect(self.success_url)


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Atualiza um ticket existente."""
    model = Ticket
    form_class = TicketForm
    template_name = 'app_tickets/ticket_edit.html'
    
    def test_func(self):
        """Verifica se o usuário pode editar o ticket."""
        obj = self.get_object()
        return self.request.user.is_staff or obj.requester == self.request.user

    def form_valid(self, form):
        """Injeta o usuário atual para o histórico antes de salvar."""
        ticket = form.save(commit=False)
        ticket._current_user = self.request.user
        ticket.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket-detail', kwargs={'pk': self.object.pk})


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deleta um ticket existente."""
    model = Ticket
    template_name = 'app_tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        """Verifica se o usuário pode deletar o ticket."""
        obj = self.get_object()
        return self.request.user.is_staff or obj.requester == self.request.user
