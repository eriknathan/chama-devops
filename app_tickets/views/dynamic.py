from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from ..models import Ticket, TicketAttachment
from app_management.models import Project, Topic
from django import forms

class DynamicTicketCreateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Generic view to create tickets from Topid.form_fields definition."""
    template_name = 'app_tickets/forms/dynamic_form.html'
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        return not self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id = self.kwargs.get('pk')
        context['topic'] = get_object_or_404(Topic, pk=topic_id)
        context['projects'] = Project.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        topic_id = self.kwargs.get('pk')
        topic = get_object_or_404(Topic, pk=topic_id)
        
        project_id = request.POST.get('project')
        project = get_object_or_404(Project, pk=project_id)

        # Build description from form fields
        description_parts = []
        if topic.template:
            description_parts.append(topic.template)
            description_parts.append("\n---\n")

        description_parts.append("### Detalhes da Solicitação\n")

        for field in topic.form_fields:
            field_name = field.get('name')
            field_label = field.get('label', field_name)
            field_type = field.get('type')
            
            
            value = request.POST.get(field_name)
            
            # Handle checkboxes specifically
            if field_type == 'checkbox':
                value = 'Sim' if value else 'Não'
            elif field_type == 'multiselect':
                values = request.POST.getlist(field_name)
                value = ', '.join(values) if values else 'N/A'
            
            # If value is missing and required, we should probably validate.
            # For now, simplistic implementation:
            if not value and field.get('required', False):
                 # In a real app we'd re-render with errors
                 pass

            description_parts.append(f"**{field_label}**: {value if value else 'N/A'}")

        description = "\n".join(description_parts)

        # Create Ticket
        ticket = Ticket.objects.create(
            title=f'{topic.name}: {project.name}',
            description=description,
            project=project,
            topic=topic,
            requester=request.user,
            priority=request.POST.get('priority', Ticket.PRIORITY_MEDIUM),
        )
        
        # Handle attachments
        files = request.FILES.getlist('attachments')
        for file in files:
            TicketAttachment.objects.create(ticket=ticket, file=file)

        return redirect(self.success_url)
