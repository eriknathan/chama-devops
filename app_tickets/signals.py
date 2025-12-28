from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Ticket

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
