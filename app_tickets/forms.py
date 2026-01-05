from django import forms
from .models import Ticket, TicketAttachment, Comment

class MultipleFileInput(forms.ClearableFileInput):
    """Widget para selecionar múltiplos arquivos."""
    allow_multiple_selected = True

class TicketForm(forms.ModelForm):
    """Formulário para Tickets."""
    # Field to handle file upload manually in the view
    attachment = forms.FileField(
        label='Anexos (opcional)', 
        required=False, 
        widget=MultipleFileInput()
    )

    class Meta:
        model = Ticket
        fields = ['project', 'topic', 'title', 'description', 'attachment']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-checkbox h-4 w-4 text-indigo-600 transition duration-150 ease-in-out'
            else:
                field.widget.attrs['class'] = 'appearance-none rounded-lg relative block w-full px-3 py-2 border border-border bg-background placeholder-muted-foreground text-foreground focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'


class CommentForm(forms.ModelForm):
    """Formulário para Comentários."""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva seu comentário...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
             field.widget.attrs['class'] = 'appearance-none rounded-lg relative block w-full px-3 py-2 border border-border bg-background placeholder-muted-foreground text-foreground focus:outline-none focus:ring-primary focus:border-primary sm:text-sm'
