from django.contrib import admin
from .models import Ticket, TicketAttachment

class TicketAttachmentInline(admin.TabularInline):
    """Inline para anexos de app_tickets."""
    model = TicketAttachment
    extra = 1

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin para Tickets."""
    list_display = ('id', 'title', 'status', 'requester', 'assignee', 'created_at')
    list_filter = ('status', 'project', 'topic')
    search_fields = ('title', 'description', 'requester__email')
    inlines = [TicketAttachmentInline]
