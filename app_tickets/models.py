from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from app_management.models import BaseModel, Project, Topic


class Ticket(BaseModel):
    """Modelo de Ticket."""
    STATUS_OPEN = 'OPEN'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_BLOCKED = 'BLOCKED'
    STATUS_DONE = 'DONE'

    STATUS_CHOICES = (
        (STATUS_OPEN, _('Aberto')),
        (STATUS_ACCEPTED, _('Aceito')),
        (STATUS_IN_PROGRESS, _('Em andamento')),
        (STATUS_BLOCKED, _('Travado')),
        (STATUS_DONE, _('Finalizado')),
    )

    PRIORITY_LOW = 'LOW'
    PRIORITY_MEDIUM = 'MEDIUM'
    PRIORITY_HIGH = 'HIGH'
    PRIORITY_CRITICAL = 'CRITICAL'

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, _('Baixa')),
        (PRIORITY_MEDIUM, _('Média')),
        (PRIORITY_HIGH, _('Alta')),
        (PRIORITY_CRITICAL, _('Crítica')),
    )

    title = models.CharField(_('Título'), max_length=200)
    description = models.TextField(_('Descrição'))
    
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_tickets', verbose_name=_('Solicitante'))
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets', verbose_name=_('Responsável'))
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='app_tickets', verbose_name=_('Projeto'))
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='app_tickets', verbose_name=_('Tópico'))
    
    priority = models.CharField(_('Prioridade'), max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)

    # SLA Metrics
    first_response_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)



    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.pk} - {self.title}"


class TicketAttachment(models.Model):
    """Modelo de Anexo do Ticket."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='app_tickets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Anexo')
        verbose_name_plural = _('Anexos')
    
    def __str__(self):
        return f"Anexo de {self.ticket}"


class Comment(BaseModel):
    """Modelo de Comentário."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Ticket'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Autor'))
    content = models.TextField(_('Comentário'))
    is_internal = models.BooleanField(_('Interno'), default=False, help_text=_('Apenas visível para equipe DevOps'))

    class Meta:
        verbose_name = _('Comentário')
        verbose_name_plural = _('Comentários')
        ordering = ['created_at']

    def __str__(self):
        return f"Comentário de {self.author} em {self.ticket}"


class TicketHistory(models.Model):
    """Modelo para histórico de mudanças no Ticket."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50)  # e.g., 'status_changed', 'assignee_changed'
    old_value = models.CharField(max_length=200, blank=True, null=True)
    new_value = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Histórico de {self.ticket} em {self.created_at}"
