from django.views.generic import UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from ..models import Ticket
from ..forms import TicketForm
from app_management.models import Topic
import json

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


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Atualiza um ticket existente."""
    model = Ticket
    form_class = TicketForm
    template_name = 'app_tickets/ticket_edit.html'
    
    def test_func(self):
        """Verifica se o usuário pode editar o ticket."""
        obj = self.get_object()
        return self.request.user.is_staff or obj.requester == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topics = Topic.objects.all()
        # Create a dictionary of {topic_id: template_text}
        topic_templates = {topic.pk: topic.template for topic in topics if topic.template}
        context['topic_templates'] = json.dumps(topic_templates)
        
        # Create a dictionary of {topic_id: form_fields_json}
        topic_forms = {topic.pk: topic.form_fields for topic in topics if topic.form_fields}
        context['topic_forms'] = json.dumps(topic_forms)
        
        return context

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


class TicketPDFView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Gera um PDF do ticket."""
    model = Ticket
    template_name = 'app_tickets/ticket_pdf.html'
    context_object_name = 'ticket'

    def test_func(self):
        """A mesma permissão do detalhe: staff ou dono."""
        obj = self.get_object()
        return self.request.user.is_staff or obj.requester == self.request.user

    def render_to_response(self, context, **response_kwargs):
        """Renderiza o template para PDF e retorna como download."""
        from django.template.loader import render_to_string
        from weasyprint import HTML
        from django.http import HttpResponse

        html_string = render_to_string(self.template_name, context, request=self.request)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket-{self.object.pk}.pdf"'
        
        HTML(string=html_string, base_url=self.request.build_absolute_uri('/')).write_pdf(response)
        return response
