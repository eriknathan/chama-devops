from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from ..models import Ticket, TicketAttachment
from app_management.models import Project, Topic


class RepositoryFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Formulário customizado para Solicitação de Novo Repositório."""
    model = Ticket
    fields = []  # Não usamos o formulário padrão
    template_name = 'app_tickets/forms/repository_form.html'
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        return not self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        try:
            context['topic'] = Topic.objects.get(name='Solicitação de Novo Repositório')
        except Topic.DoesNotExist:
            pass
        return context

    def post(self, request, *args, **kwargs):
        # Get the selected project
        project_id = request.POST.get('project')
        project = get_object_or_404(Project, pk=project_id)
        
        # Get the topic
        try:
            topic = Topic.objects.get(name='Solicitação de Novo Repositório')
        except Topic.DoesNotExist:
            topic = None

        # Build description from form data
        nome_repo = request.POST.get('nome_repositorio', '')
        descricao = request.POST.get('descricao', '')
        squad = request.POST.get('squad_responsavel', '')
        visibilidade = request.POST.get('visibilidade', '')
        linguagem = request.POST.get('linguagem_principal', '')
        template = request.POST.get('template', '')
        times_acesso = request.POST.get('times_acesso', '')
        acesso_grafana = request.POST.get('acesso_grafana', 'Não')

        description = f"""### Dados Gerais do Repositório

**Nome do Repositório**: {nome_repo}

**Descrição do Projeto**: {descricao}

**Squad/Time Responsável**: {squad}

---

### Configurações do Repositório

**Visibilidade**: {visibilidade}

**Linguagem Principal**: {linguagem}

**Template**: {template if template else 'Nenhum (criar do zero)'}

---

### Acessos Iniciais

**Times/Usuários com Acesso Write**:
{times_acesso}

**Liberar Acesso Grafana**: {acesso_grafana}
"""

        # Create the ticket
        ticket = Ticket.objects.create(
            title=f'Novo Repositório: {nome_repo}',
            description=description,
            project=project,
            topic=topic,
            requester=request.user,
            priority=request.POST.get('priority', Ticket.PRIORITY_MEDIUM),
        )
        ticket._current_user = request.user
        ticket.save()

        # Handle attachments
        files = request.FILES.getlist('attachments')
        for file in files:
            TicketAttachment.objects.create(ticket=ticket, file=file)

        return redirect(self.success_url)


class GitHubAccessFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Formulário customizado para Gerenciamento de Acesso ao GitHub."""
    model = Ticket
    fields = []
    template_name = 'app_tickets/forms/github_access_form.html'
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        return not self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        try:
            context['topic'] = Topic.objects.get(name='Gerenciamento de Acesso ao GitHub')
        except Topic.DoesNotExist:
            pass
        return context

    def post(self, request, *args, **kwargs):
        # Get the selected project
        project_id = request.POST.get('project')
        project = get_object_or_404(Project, pk=project_id)
        
        # Get the topic
        try:
            topic = Topic.objects.get(name='Gerenciamento de Acesso ao GitHub')
        except Topic.DoesNotExist:
            topic = None

        # Build description from form data
        tipo = request.POST.get('tipo_solicitacao', '')
        nome = request.POST.get('nome_completo', '')
        email = request.POST.get('email_corporativo', '')
        github_user = request.POST.get('github_username', '')
        repositorios = request.POST.get('repositorios', '')
        permissao = request.POST.get('nivel_permissao', '')
        justificativa = request.POST.get('justificativa', '')

        description = f"""### Tipo de Solicitação

**Ação**: {tipo} acesso

---

### Dados do Usuário

**Nome Completo**: {nome}

**E-mail Corporativo**: {email}

**Username GitHub**: @{github_user}

---

### Dados do Acesso

**Repositório(s)**:
{repositorios}

**Nível de Permissão**: {permissao}

---

### Justificativa

{justificativa}
"""

        # Create the ticket
        ticket = Ticket.objects.create(
            title=f'{tipo} Acesso GitHub: @{github_user}',
            description=description,
            project=project,
            topic=topic,
            requester=request.user,
            priority=request.POST.get('priority', Ticket.PRIORITY_MEDIUM),
        )
        ticket._current_user = request.user
        ticket.save()

        # Handle attachments
        files = request.FILES.getlist('attachments')
        for file in files:
            TicketAttachment.objects.create(ticket=ticket, file=file)

        return redirect(self.success_url)


class DowntimeFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Formulário customizado para Reporte de Indisponibilidade."""
    model = Ticket
    fields = []
    template_name = 'app_tickets/forms/downtime_form.html'
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        return not self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        try:
            context['topic'] = Topic.objects.get(name='Reporte de Indisponibilidade')
        except Topic.DoesNotExist:
            pass
        return context

    def post(self, request, *args, **kwargs):
        # Get selected project
        project_id = request.POST.get('project')
        project = get_object_or_404(Project, pk=project_id)
        
        # Get topic
        try:
            topic = Topic.objects.get(name='Reporte de Indisponibilidade')
        except Topic.DoesNotExist:
            topic = None

        # Build description
        nome = request.POST.get('nome_servico', '')
        url = request.POST.get('url_erro', '')
        ambiente = request.POST.get('ambiente', '')
        sintoma = request.POST.get('sintoma_principal', '')
        desc_sintomas = request.POST.get('descricao_sintomas', '')
        msg_erro = request.POST.get('mensagem_erro', '')
        impacto = request.POST.get('quem_afetado', '') # Changed key to match form
        horario = request.POST.get('horario_inicio', '')
        
        # Get priority from form
        priority = request.POST.get('priority', Ticket.PRIORITY_MEDIUM)

        description = f"""### Serviço Afetado

**Serviço**: {nome}
**URL**: {url}
**Ambiente**: {ambiente}

---

### Sintomas

**Sintoma Principal**: {sintoma}
**Descrição**: {desc_sintomas}
**Mensagem de Erro**: {msg_erro}

---

### Impacto

**Afetados**: {impacto}
**Início**: {horario}
"""

        # Create ticket
        ticket = Ticket.objects.create(
            title=f'Indisponibilidade: {nome} ({sintoma})',
            description=description,
            project=project,
            topic=topic,
            requester=request.user,
            priority=priority,
        )
        ticket._current_user = request.user
        ticket.save()

        # Attachments
        files = request.FILES.getlist('attachments')
        for file in files:
            TicketAttachment.objects.create(ticket=ticket, file=file)

        return redirect(self.success_url)


class ProjectIntakeFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Formulário customizado para Intake de Projeto."""
    model = Ticket
    fields = []
    template_name = 'app_tickets/forms/project_intake_form.html'
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        return not self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        # Fallback to None if topic doesn't exist, logic will handle it
        try:
            context['topic'] = Topic.objects.get(name='Intake de Projeto')
        except Topic.DoesNotExist:
            context['topic'] = None
        return context

    def post(self, request, *args, **kwargs):
        # Project & Topic
        project_id = request.POST.get('project')
        project = get_object_or_404(Project, pk=project_id)
        
        try:
            topic = Topic.objects.get(name='Intake de Projeto')
        except Topic.DoesNotExist:
            topic = None

        # 2.1 Info Gerais
        nome_projeto = request.POST.get('nome_projeto', '')
        centro_custo = request.POST.get('centro_custo', '')
        tech_lead = request.POST.get('tech_lead', '')
        email_contato = request.POST.get('email_contato', '')
        data_golive = request.POST.get('data_golive', '')
        criticidade_negocio = request.POST.get('criticidade_negocio', '')

        # 2.2 Arquitetura
        tipos_app = request.POST.getlist('tipo_aplicacao')
        stack = request.POST.getlist('stack')
        stack_outro = request.POST.get('stack_outro', '')
        if stack_outro:
            stack.append(f'Outro: {stack_outro}')
        deploy_model = request.POST.get('deploy_model', '')
        repo_tipo = request.POST.get('repositorio_tipo', '')
        repo_url = request.POST.get('repositorio_url', '')

        # 2.3 Rede
        exposicao = request.POST.get('exposicao', '')
        vpn = request.POST.get('vpn', '')
        vpn_perfil = request.POST.get('vpn_perfil', '')
        dominio = request.POST.get('dominio', '')
        dominio_tipo = request.POST.get('dominio_tipo', '')
        certificado = request.POST.get('certificado', '')
        waf = request.POST.get('waf', '')
        cdn = request.POST.get('cdn', '')

        # 2.4 AWS
        aws_db = request.POST.getlist('aws_db')
        aws_cache = request.POST.getlist('aws_cache')
        aws_storage = request.POST.getlist('aws_storage')

        # 2.5 HA & Performance
        sla = request.POST.get('sla', '')
        multiaz = request.POST.get('multiaz', '')
        asg_min = request.POST.get('asg_min', '')
        asg_max = request.POST.get('asg_max', '')
        asg_metrics = request.POST.getlist('asg_metric')
        rps = request.POST.get('rps', '')
        latencia = request.POST.get('latencia', '')

        # 2.6 Obs
        obs_logs = request.POST.getlist('obs_logs')
        obs_metrics = request.POST.getlist('obs_metrics')
        obs_alerts = request.POST.getlist('obs_alerts')
        obs_dashboard = request.POST.get('obs_dashboard', '')
        observacoes = request.POST.get('observacoes', '')

        # Description Builder
        description = f"""### 2.1 Informações Gerais
**Nome do Projeto**: {nome_projeto}
**Centro de Custo**: {centro_custo}
**Tech Lead**: {tech_lead}
**E-mail**: {email_contato}
**Go-Live**: {data_golive}
**Criticidade Negócio**: {criticidade_negocio}

---

### 2.2 Arquitetura
**Tipo Aplicação**: {', '.join(tipos_app)}
**Stack**: {', '.join(stack)}
**Deploy**: {deploy_model}
**Repositório**: {repo_tipo} ({repo_url})

---

### 2.3 Rede
**Exposição**: {exposicao}
**VPN**: {vpn} ({vpn_perfil if vpn == 'Sim' else 'N/A'})
**Domínio**: {dominio} ({dominio_tipo})
**Certificado**: {certificado}
**WAF**: {waf}
**CDN**: {cdn}

---

### 2.4 Serviços AWS
**Banco de Dados**: {', '.join(aws_db) if aws_db else 'Nenhum'}
**Cache/Msg**: {', '.join(aws_cache) if aws_cache else 'Nenhum'}
**Storage**: {', '.join(aws_storage) if aws_storage else 'Nenhum'}

---

### 2.5 HA e Performance
**SLA**: {sla}
**Multi-AZ**: {multiaz}
**Auto Scaling**: {asg_min}-{asg_max} instâncias (Por: {', '.join(asg_metrics)})
**RPS**: {rps}
**Latência**: {latencia}

---

### 2.6 Observabilidade
**Logs**: {', '.join(obs_logs) if obs_logs else 'Padrão'}
**Métricas**: {', '.join(obs_metrics) if obs_metrics else 'Padrão'}
**Alertas**: {', '.join(obs_alerts) if obs_alerts else 'Nenhum'}
**Dashboard**: {obs_dashboard}

---

**Observações Adicionais**:
{observacoes}
"""

        # Priority Mapping
        priority_map = {
            'Crítico': Ticket.PRIORITY_CRITICAL,
            'Alto': Ticket.PRIORITY_HIGH,
            'Médio': Ticket.PRIORITY_MEDIUM,
            'Baixo': Ticket.PRIORITY_LOW
        }
        # Use explicit priority if provided, else map from business criticality
        form_priority = request.POST.get('priority')
        business_priority = priority_map.get(criticidade_negocio, Ticket.PRIORITY_MEDIUM)
        
        ticket = Ticket.objects.create(
            title=f'Intake: {nome_projeto}',
            description=description,
            project=project,
            topic=topic,
            requester=request.user,
            priority=form_priority or business_priority,
        )
        ticket._current_user = request.user
        ticket.save()
        
        # Attachments
        files = request.FILES.getlist('attachments')
        for file in files:
            TicketAttachment.objects.create(ticket=ticket, file=file)

        return redirect(self.success_url)

