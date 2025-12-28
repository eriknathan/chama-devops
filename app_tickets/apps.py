from django.apps import AppConfig


class TicketsConfig(AppConfig):
    """Configuração da aplicação de app_tickets."""
    name = 'app_tickets'

    def ready(self):
        import app_tickets.signals
