from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Project, Topic
import json

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin para Projetos."""
    list_display = ('name', 'created_at')
    search_fields = ('name',)


class TopicAdminForm(forms.ModelForm):
    """Formulário customizado para edição de Tópicos no Admin."""
    
    # Campos auxiliares para criar novos campos dinâmicos
    new_field_label = forms.CharField(
        label='Nome do Campo',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Nome do Usuário', 'class': 'vTextField'})
    )
    new_field_type = forms.ChoiceField(
        label='Tipo do Campo',
        required=False,
        choices=[
            ('', '-- Selecione --'),
            ('text', 'Texto'),
            ('textarea', 'Área de Texto'),
            ('select', 'Lista de Opções'),
            ('checkbox', 'Checkbox'),
        ]
    )
    new_field_placeholder = forms.CharField(
        label='Placeholder',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Texto de exemplo', 'class': 'vTextField'})
    )
    new_field_options = forms.CharField(
        label='Opções (para Lista)',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Opção1, Opção2, Opção3', 'class': 'vTextField'}),
        help_text='Separe as opções por vírgula (apenas para tipo "Lista de Opções")'
    )
    
    class Meta:
        model = Topic
        fields = ['name', 'template', 'form_fields']
        widgets = {
            'form_fields': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona campos para remoção de cada campo existente
        if self.instance and self.instance.pk and self.instance.form_fields:
            for i, field in enumerate(self.instance.form_fields):
                self.fields[f'remove_field_{i}'] = forms.BooleanField(
                    label=f'Remover "{field.get("label", "")}"',
                    required=False,
                    initial=False
                )
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Pega os campos existentes
        current_fields = instance.form_fields or []
        
        # Remove campos marcados para remoção
        if self.instance.pk:
            fields_to_keep = []
            for i, field in enumerate(current_fields):
                if not self.cleaned_data.get(f'remove_field_{i}', False):
                    fields_to_keep.append(field)
            current_fields = fields_to_keep
        
        # Adiciona novo campo se preenchido
        new_label = self.cleaned_data.get('new_field_label', '').strip()
        new_type = self.cleaned_data.get('new_field_type', '')
        
        if new_label and new_type:
            new_field = {
                'label': new_label,
                'type': new_type,
            }
            
            placeholder = self.cleaned_data.get('new_field_placeholder', '').strip()
            if placeholder:
                new_field['placeholder'] = placeholder
            
            if new_type == 'select':
                options_str = self.cleaned_data.get('new_field_options', '')
                if options_str:
                    options = [opt.strip() for opt in options_str.split(',') if opt.strip()]
                    new_field['options'] = options
            
            current_fields.append(new_field)
        
        instance.form_fields = current_fields
        
        if commit:
            instance.save()
        return instance


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin para Tópicos."""
    form = TopicAdminForm
    list_display = ('name', 'field_count', 'created_at')
    search_fields = ('name',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'template')
        }),
        ('Campos Dinâmicos Atuais', {
            'fields': ('current_fields_display',),
            'description': 'Campos que aparecem quando este tópico é selecionado no formulário de ticket.'
        }),
        ('Gerenciar Campos', {
            'fields': ('form_fields',),
            'classes': ('collapse',),
        }),
        ('Adicionar Novo Campo', {
            'fields': ('new_field_label', 'new_field_type', 'new_field_placeholder', 'new_field_options'),
            'description': 'Preencha os campos abaixo e salve para adicionar um novo campo dinâmico.'
        }),
    )
    
    readonly_fields = ('current_fields_display',)
    
    def field_count(self, obj):
        """Retorna a quantidade de campos dinâmicos."""
        if obj.form_fields:
            return len(obj.form_fields)
        return 0
    field_count.short_description = 'Campos Dinâmicos'
    
    def current_fields_display(self, obj):
        """Exibe os campos atuais em formato legível."""
        from django.utils.safestring import mark_safe
        
        if not obj.form_fields:
            return mark_safe('<em>Nenhum campo dinâmico configurado.</em>')
        
        html = '<table style="width:100%; border-collapse: collapse;">'
        html += '<tr style="background: #f0f0f0;"><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Tipo</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Placeholder</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Opções</th></tr>'
        
        type_labels = {
            'text': 'Texto',
            'textarea': 'Área de Texto',
            'select': 'Lista de Opções',
            'checkbox': 'Checkbox',
        }
        
        for i, field in enumerate(obj.form_fields):
            label = field.get('label', '-')
            field_type = type_labels.get(field.get('type', ''), field.get('type', '-'))
            placeholder = field.get('placeholder', '-')
            options = ', '.join(field.get('options', [])) if field.get('options') else '-'
            
            html += f'<tr><td style="padding: 8px; border: 1px solid #ddd;">{label}</td><td style="padding: 8px; border: 1px solid #ddd;">{field_type}</td><td style="padding: 8px; border: 1px solid #ddd;">{placeholder}</td><td style="padding: 8px; border: 1px solid #ddd;">{options}</td></tr>'
        
        html += '</table>'
        html += '<p style="margin-top: 10px; color: #666;"><strong>Para remover campos:</strong> Edite o JSON diretamente na seção "Gerenciar Campos" abaixo.</p>'
        
        return mark_safe(html)
    current_fields_display.short_description = 'Campos Configurados'

