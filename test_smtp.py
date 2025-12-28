import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_email():
    """Testa a configuração de envio de emails via SMTP."""
    print(f"Testing email config:")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"User: {settings.EMAIL_HOST_USER}")
    print(f"Backend: {settings.EMAIL_BACKEND}")
    
    try:
        send_mail(
            'Test Email from ChamaDevOps',
            'This is a test email to verify SMTP configuration.',
            settings.DEFAULT_FROM_EMAIL,
            ['enobtech.empresa@gmail.com'], # Sending to the admin email for verification
            fail_silently=False,
        )
        print("SUCCESS: Email sent successfully!")
    except Exception as e:
        print(f"ERROR: Failed to send email.\n{e}")

if __name__ == "__main__":
    test_email()
