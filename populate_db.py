import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from app_management.models import Topic, Project
from app_tickets.models import Ticket

User = get_user_model()

def populate():
    """Popula o banco de dados com dados massivos e diversificados."""
    print("Iniciando população do banco de dados...")

    # --- 1. Usuários Administrativos e DevOps ---
    admin_email = 'admin@chamadevops.com'
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(admin_email, 'admin')
        print(f'Superuser created: {admin_email}')

    devs = [
        ('maria@email.com', 'Maria Helena'),
        ('joao@email.com', 'João Felipe'),
        ('pedro@email.com', 'Pedro Santos'),
        ('lucas@email.com', 'Lucas Silva'),
        ('ana@email.com', 'Ana Costa')
    ]
    
    dev_users = []
    for email, name in devs:
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': name.split()[0],
                'last_name': " ".join(name.split()[1:]),
                'is_staff': True  # DevOps/Staff
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f'Developer created: {email}')
        dev_users.append(user)

    # --- 2. Usuários Comuns (Clientes/Solicitantes) ---
    common_users_data = [
        ('cliente1@empresa.com', 'Carlos Cliente'),
        ('cliente2@empresa.com', 'Beatriz Souza'),
        ('gerente@loja.com', 'Fernanda Lima'),
        ('suporte@parceiro.com', 'Roberto Dias'),
        ('marketing@interno.com', 'Juliana Mello'),
        ('vendas@interno.com', 'Ricardo Oliveira'),
        ('rh@empresa.com', 'Patricia Gomes'),
        ('financeiro@empresa.com', 'Marcelo Vieira'),
        ('operacoes@logistica.com', 'Eduardo Ramos'),
        ('loja01@rede.com', 'Amanda Nunes'),
        ('loja02@rede.com', 'Bruno Castro'),
        ('regional@rede.com', 'Camila Rocha'),
        ('diretoria@empresa.com', 'Daniel Martins'),
        ('auditoria@externo.com', 'Eliane Moura'),
        ('consultor@externo.com', 'Fabio Ribeiro')
    ]

    common_users = []
    for email, name in common_users_data:
        user, created = User.objects.get_or_create(
            email=email, 
            defaults={
                'first_name': name.split()[0],
                'last_name': " ".join(name.split()[1:])
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f'Common User created: {email}')
        common_users.append(user)

    # --- 3. Tópicos ---
    topics = ['DevOps', 'Frontend', 'Backend', 'Infraestrutura', 'Banco de Dados', 'QA', 'Segurança', 'Mobile', 'Design', 'Redes']
    topic_objs = []
    for topic_name in topics:
        topic, created = Topic.objects.get_or_create(name=topic_name)
        topic_objs.append(topic)

    # --- 4. Projetos ---
    projects_list = [
        'Chama App', 'Site Institucional', 'Legacy System', 
        'Portal do Cliente', 'API de Pagamentos', 'Sistema de Estoque',
        'App Logística (Android)', 'App Logística (iOS)', 'Dashboard Financeiro',
        'Intranet Corporativa', 'CRM Vendas', 'Bot de Atendimento',
        'Migração Cloud', 'Data Lake'
    ]
    
    project_objs = []
    for proj_name in projects_list:
        project, created = Project.objects.get_or_create(name=proj_name)
        if created:
            print(f'Project created: {proj_name}')
            # Assign random members
            members_count = random.randint(2, len(dev_users))
            project.members.add(*random.sample(dev_users, members_count))
        project_objs.append(project)

    # --- 5. Tickets Massivos ---
    print("Gerando tickets históricos (pode demorar um pouco)...")
    
    # Status weighted towards OPEN (50%)
    statuses = [Ticket.STATUS_OPEN] * 50 + [Ticket.STATUS_IN_PROGRESS] * 20 + \
               [Ticket.STATUS_DONE] * 20 + [Ticket.STATUS_BLOCKED] * 5 + [Ticket.STATUS_ACCEPTED] * 5
    
    titles_prefixes = ['Erro em', 'Ajuste em', 'Melhoria no', 'Atualização de', 'Falha no', 'Solicitação de', 'Bug no']
    titles_suffixes = ['Login', 'Cadastro', 'Dashboard', 'Relatório', 'API', 'Banco', 'Servidor', 'Layout', 'Botão', 'Pagamento']

    total_new_tickets = 150  # Total to generate
    
    count_created = 0
    now = timezone.now()

    for _ in range(total_new_tickets):
        # Generate Random Properties
        project = random.choice(project_objs)
        topic = random.choice(topic_objs)
        requester = random.choice(common_users)
        status = random.choice(statuses)
        
        # Random Date within last 12 months
        days_back = random.randint(0, 365)
        created_date = now - timedelta(days=days_back)
        
        # Title
        title = f"{random.choice(titles_prefixes)} {random.choice(titles_suffixes)} - {project.name}"
        
        # Logic for assignee based on status
        assignee = None
        if status != Ticket.STATUS_OPEN:
            # If worked on, probably has an assignee (a dev)
            assignee = random.choice(dev_users) if dev_users else None

        # Check duplication loosely to avoid exact spam
        # We allow same title if date is different, but here we enforce uniqueness on title+project roughly
        # Actually random title is common. We just create it.
        
        ticket = Ticket.objects.create(
            title=title,
            description=f"Descrição detalhada sobre {title}. Necessário verificar logs e reproduzir o erro. Criado em {created_date.date()}.",
            project=project,
            topic=topic,
            requester=requester,
            assignee=assignee,
            status=status
        )
        
        # Manually update created_at using update() to bypass auto_now_add
        Ticket.objects.filter(pk=ticket.pk).update(created_at=created_date)
        count_created += 1

    print(f"População concluída! {count_created} novos tickets gerados.")

if __name__ == '__main__':
    populate()
