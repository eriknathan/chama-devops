from django.utils.html import strip_tags
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Ticket, TicketHistory

@receiver(pre_save, sender=Ticket)
def track_changes(sender, instance, **kwargs):
    """Captura o estado anterior e atualiza SLAs."""
    # SLA Logic
    if instance.status in [Ticket.STATUS_ACCEPTED, Ticket.STATUS_IN_PROGRESS] and not instance.first_response_at:
        instance.first_response_at = timezone.now()
    
    if instance.status == Ticket.STATUS_DONE and not instance.resolved_at:
        instance.resolved_at = timezone.now()

    if instance.pk:
        try:
            old_instance = Ticket.objects.get(pk=instance.pk)
            instance._old_instance = old_instance
        except Ticket.DoesNotExist:
            pass

@receiver(post_save, sender=Ticket)
def log_changes(sender, instance, created, **kwargs):
    """Registra as mudanças no histórico após salvar."""
    user = getattr(instance, '_current_user', None)

    if created:
        TicketHistory.objects.create(
            ticket=instance,
            user=user,
            action='created',
            new_value='Ticket criado'
        )
    elif hasattr(instance, '_old_instance'):
        old = instance._old_instance
        
        # Monitor Status Change
        if old.status != instance.status:
            TicketHistory.objects.create(
                ticket=instance,
                user=user,
                action='status_changed',
                old_value=old.get_status_display(),
                new_value=instance.get_status_display()
            )
        
        # Monitor Priority Change
        if old.priority != instance.priority:
            TicketHistory.objects.create(
                ticket=instance,
                user=user,
                action='priority_changed',
                old_value=old.get_priority_display(),
                new_value=instance.get_priority_display()
            )

        # Monitor Assignee Change
        if old.assignee != instance.assignee:
            old_name = old.assignee.get_full_name() if old.assignee else 'Não atribuído'
            new_name = instance.assignee.get_full_name() if instance.assignee else 'Não atribuído'
            
            TicketHistory.objects.create(
                ticket=instance,
                user=user,
                action='assignee_changed',
                old_value=old_name,
                new_value=new_name
            )

@receiver(post_save, sender=Ticket)
def send_ticket_creation_email(sender, instance, created, **kwargs):
    """Envia email quando um novo ticket é criado."""
    if created:
        subject = f'Novo Ticket: #{instance.pk} - {instance.title}'
        
        # Context for the template
        context = {
            'ticket': instance,
            'protocol': 'http', # Hardcoding for now/dev, ideally use request or sites framework
            'domain': '127.0.0.1:8000', 
        }
        
        # Render HTML content
        html_message = render_to_string('emails/ticket_created.html', context)
        # Create plain text version as fallback
        plain_message = strip_tags(html_message)
        
        recipient_list = []
        if instance.assignee:
            recipient_list.append(instance.assignee.email)
        
        recipient_list.append(instance.requester.email)
        
        # Also always notify the admin/company email as per request
        admin_email = settings.DEFAULT_FROM_EMAIL
        # Extract email if format is "Name <email>"
        if '<' in admin_email:
            admin_email = admin_email.split('<')[1].strip('>')
        
        if admin_email not in recipient_list:
            recipient_list.append(admin_email)
        
        if recipient_list:
            send_mail(
                subject,
                plain_message, # Plain text version
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                html_message=html_message, # HTML version
                fail_silently=True,
            )
