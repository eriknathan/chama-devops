from django import forms
from .models import Project, Topic

class TailwindFormMixin:
    """Mixin para aplicar estilos Tailwind aos campos do formulário."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-checkbox h-4 w-4 text-indigo-600 transition duration-150 ease-in-out'
            else:
                field.widget.attrs['class'] = 'appearance-none rounded-lg relative block w-full px-3 py-2 border border-slate-300 placeholder-slate-500 text-slate-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'

from django.contrib.auth import get_user_model

class ProjectForm(TailwindFormMixin, forms.ModelForm):
    """Formulário para Projetos."""
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Desenvolvedores'
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'manager', 'members']

class TopicForm(TailwindFormMixin, forms.ModelForm):
    """Formulário para Tópicos."""
    class Meta:
        model = Topic
        fields = ['name']
