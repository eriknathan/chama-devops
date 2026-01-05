import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app_management.models import Topic

# Criar novo tópico para Reporte de Indisponibilidade
topic = Topic.objects.create(
    name='Reporte de Indisponibilidade',
    template='',
    form_fields=[
        {
            'type': 'text',
            'label': 'Nome do Sistema/Serviço',
            'placeholder': 'Ex: Portal do Cliente, API de Pagamentos'
        },
        {
            'type': 'text',
            'label': 'URL (Link) onde ocorre o erro',
            'placeholder': 'https://exemplo.com/pagina'
        },
        {
            'type': 'select',
            'label': 'Ambiente',
            'options': ['Produção', 'Homologação/Staging', 'Dev', 'Outro']
        },
        {
            'type': 'select',
            'label': 'O que está acontecendo?',
            'options': ['Site não carrega', 'Lentidão extrema', 'Erro 404/500', 'Funcionalidade quebrada', 'Outro']
        },
        {
            'type': 'textarea',
            'label': 'Mensagem de erro exibida (se houver)',
            'placeholder': 'Copie e cole a mensagem de erro aqui'
        },
        {
            'type': 'select',
            'label': 'Quem está sendo afetado?',
            'options': ['Apenas eu', 'Vários usuários', 'Todos os usuários (Parada Total)']
        },
        {
            'type': 'text',
            'label': 'Desde quando (Horário aproximado)',
            'placeholder': 'Ex: 14:30 de hoje'
        }
    ]
)
print(f'Tópico criado com sucesso! ID: {topic.pk}, Nome: {topic.name}')
