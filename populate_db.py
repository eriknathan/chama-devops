import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from app_management.models import Topic

User = get_user_model()

def populate():
    """Popula o banco de dados com usuário admin e tópicos."""
    print("Iniciando população do banco de dados...")

    # --- 1. Usuário Administrativo ---
    admin_email = 'admin@chamadevops.com'
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(admin_email, 'admin')
        print(f'Superuser created: {admin_email}')
    else:
        print(f'Superuser already exists: {admin_email}')

    # --- 2. Tópicos ---
    topics_data = [
        {
            'name': 'Gerenciamento de Acesso ao GitHub',
            'template': '''Utilize este tópico para **solicitar a adição ou remoção de acesso a repositórios do GitHub**.
Ao abrir a solicitação, informe obrigatoriamente os dados abaixo:

- **Tipo de solicitação**: indique se o acesso deve ser **adicionado** ou **removido**.
- **Dados do usuário**:
    - Nome completo
    - E-mail corporativo
    - Username do GitHub (exemplo: @usuario)
- **Dados do acesso**:
    - Link do(s) repositório(s) ao qual o acesso será concedido ou removido
    - Nível de permissão desejado: **Leitura (Read)**, **Escrita (Write)** ou **Administrador (Admin)**
- **Motivo ou justificativa** da solicitação.

⚠️ Solicitações incompletas ou sem justificativa poderão ser devolvidas para ajuste.''',
            'form_fields': [
                {'name': 'tipo_solicitacao', 'type': 'select', 'label': 'Tipo de Solicitação', 'options': ['Adicionar', 'Remover'], 'required': True},
                {'name': 'nome_completo', 'type': 'text', 'label': 'Nome Completo', 'required': True},
                {'name': 'email_corporativo', 'type': 'email', 'label': 'E-mail Corporativo', 'required': True},
                {'name': 'github_username', 'type': 'text', 'label': 'Username do GitHub', 'required': True},
                {'name': 'repositorios', 'type': 'textarea', 'label': 'Link dos Repositórios', 'required': True},
                {'name': 'nivel_permissao', 'type': 'select', 'label': 'Nível de Permissão', 'options': ['Read', 'Write', 'Admin'], 'required': True},
                {'name': 'justificativa', 'type': 'textarea', 'label': 'Motivo/Justificativa', 'required': True}
            ]
        },
        {
            'name': 'Provisionamento de Servidor/VM',
            'template': '''Utilize este tópico para **solicitar a criação de novos servidores ou máquinas virtuais**.

Informe obrigatoriamente:

- **Ambiente**: Desenvolvimento, Homologação ou Produção
- **Especificações**:
    - Sistema Operacional (ex: Ubuntu 22.04, Windows Server 2022)
    - vCPUs
    - Memória RAM (GB)
    - Armazenamento (GB)
- **Finalidade**: descreva o uso do servidor
- **Responsável técnico**: nome e e-mail
- **Prazo desejado** para entrega

⚠️ Solicitações de produção requerem aprovação do gestor.''',
            'form_fields': [
                {'name': 'ambiente', 'type': 'select', 'label': 'Ambiente', 'options': ['Desenvolvimento', 'Homologação', 'Produção'], 'required': True},
                {'name': 'sistema_operacional', 'type': 'text', 'label': 'Sistema Operacional', 'required': True},
                {'name': 'vcpus', 'type': 'number', 'label': 'vCPUs', 'required': True},
                {'name': 'memoria_ram', 'type': 'number', 'label': 'Memória RAM (GB)', 'required': True},
                {'name': 'armazenamento', 'type': 'number', 'label': 'Armazenamento (GB)', 'required': True},
                {'name': 'finalidade', 'type': 'textarea', 'label': 'Finalidade', 'required': True}
            ]
        },
        {
            'name': 'Deploy em Produção',
            'template': '''Utilize este tópico para **solicitar deploy de aplicações em ambiente de produção**.

Informe obrigatoriamente:

- **Aplicação**: nome do projeto/serviço
- **Versão/Tag**: versão a ser deployada (ex: v1.2.3)
- **Branch**: branch do repositório
- **Changelog**: resumo das alterações
- **Janela de deploy**: data e horário preferencial
- **Rollback plan**: procedimento em caso de falha

⚠️ Deploys em produção requerem aprovação do tech lead.''',
            'form_fields': [
                {'name': 'aplicacao', 'type': 'text', 'label': 'Nome da Aplicação', 'required': True},
                {'name': 'versao', 'type': 'text', 'label': 'Versão/Tag', 'required': True},
                {'name': 'branch', 'type': 'text', 'label': 'Branch', 'required': True},
                {'name': 'changelog', 'type': 'textarea', 'label': 'Changelog', 'required': True},
                {'name': 'janela_deploy', 'type': 'datetime', 'label': 'Janela de Deploy', 'required': True}
            ]
        },
        {
            'name': 'Incidente de Infraestrutura',
            'template': '''Utilize este tópico para **reportar incidentes ou problemas de infraestrutura**.

Informe obrigatoriamente:

- **Severidade**: Crítico, Alto, Médio ou Baixo
- **Serviços afetados**: liste os serviços/aplicações impactados
- **Início do incidente**: data e hora aproximada
- **Sintomas observados**: descreva o comportamento anormal
- **Impacto**: descreva o impacto para usuários/negócio
- **Ações já realizadas**: o que já foi tentado

🚨 Incidentes críticos devem ser comunicados também via Slack #incidents.''',
            'form_fields': [
                {'name': 'severidade', 'type': 'select', 'label': 'Severidade', 'options': ['Crítico', 'Alto', 'Médio', 'Baixo'], 'required': True},
                {'name': 'servicos_afetados', 'type': 'textarea', 'label': 'Serviços Afetados', 'required': True},
                {'name': 'inicio_incidente', 'type': 'datetime', 'label': 'Início do Incidente', 'required': True},
                {'name': 'sintomas', 'type': 'textarea', 'label': 'Sintomas Observados', 'required': True},
                {'name': 'impacto', 'type': 'textarea', 'label': 'Impacto', 'required': True}
            ]
        },
        {
            'name': 'Liberação de Porta/Firewall',
            'template': '''Utilize este tópico para **solicitar liberação de portas ou regras de firewall**.

Informe obrigatoriamente:

- **Ambiente**: Desenvolvimento, Homologação ou Produção
- **IP/Range de origem**: de onde virá o tráfego
- **IP/Hostname de destino**: servidor que receberá o tráfego
- **Porta(s)**: número da(s) porta(s) e protocolo (TCP/UDP)
- **Direção**: Inbound ou Outbound
- **Justificativa**: motivo da liberação
- **Prazo**: temporário ou permanente

⚠️ Liberações em produção requerem aprovação de segurança.''',
            'form_fields': [
                {'name': 'ambiente', 'type': 'select', 'label': 'Ambiente', 'options': ['Desenvolvimento', 'Homologação', 'Produção'], 'required': True},
                {'name': 'ip_origem', 'type': 'text', 'label': 'IP/Range de Origem', 'required': True},
                {'name': 'ip_destino', 'type': 'text', 'label': 'IP/Hostname de Destino', 'required': True},
                {'name': 'portas', 'type': 'text', 'label': 'Porta(s) e Protocolo', 'required': True},
                {'name': 'direcao', 'type': 'select', 'label': 'Direção', 'options': ['Inbound', 'Outbound'], 'required': True},
                {'name': 'justificativa', 'type': 'textarea', 'label': 'Justificativa', 'required': True}
            ]
        },
        {
            'name': 'Criação de Pipeline CI/CD',
            'template': '''Utilize este tópico para **solicitar criação ou modificação de pipelines CI/CD**.

Informe obrigatoriamente:

- **Repositório**: link do repositório
- **Tipo de pipeline**: CI, CD ou ambos
- **Tecnologias**: linguagem, framework, ferramentas de build
- **Ambientes de deploy**: dev, staging, prod
- **Testes requeridos**: unit, integration, e2e
- **Notificações**: Slack channel, e-mails

📌 Inclua o arquivo de configuração existente se houver (Jenkinsfile, .gitlab-ci.yml, etc).''',
            'form_fields': [
                {'name': 'repositorio', 'type': 'text', 'label': 'Link do Repositório', 'required': True},
                {'name': 'tipo_pipeline', 'type': 'select', 'label': 'Tipo de Pipeline', 'options': ['CI', 'CD', 'CI/CD'], 'required': True},
                {'name': 'tecnologias', 'type': 'textarea', 'label': 'Tecnologias Utilizadas', 'required': True},
                {'name': 'ambientes', 'type': 'textarea', 'label': 'Ambientes de Deploy', 'required': True}
            ]
        },
        {
            'name': 'Backup e Restore de Dados',
            'template': '''Utilize este tópico para **solicitar backup ou restore de dados**.

Informe obrigatoriamente:

- **Tipo de solicitação**: Backup ou Restore
- **Sistema/Banco**: nome do sistema ou banco de dados
- **Ambiente**: Desenvolvimento, Homologação ou Produção
- **Data de referência**: para restore, informe a data do backup desejado
- **Justificativa**: motivo da solicitação
- **Urgência**: Normal ou Urgente

⚠️ Restores em produção requerem aprovação do DBA e gestor.''',
            'form_fields': [
                {'name': 'tipo_solicitacao', 'type': 'select', 'label': 'Tipo de Solicitação', 'options': ['Backup', 'Restore'], 'required': True},
                {'name': 'sistema_banco', 'type': 'text', 'label': 'Sistema/Banco de Dados', 'required': True},
                {'name': 'ambiente', 'type': 'select', 'label': 'Ambiente', 'options': ['Desenvolvimento', 'Homologação', 'Produção'], 'required': True},
                {'name': 'data_referencia', 'type': 'date', 'label': 'Data de Referência', 'required': False},
                {'name': 'justificativa', 'type': 'textarea', 'label': 'Justificativa', 'required': True}
            ]
        },
        {
            'name': 'Monitoramento e Alertas',
            'template': '''Utilize este tópico para **solicitar configuração de monitoramento ou alertas**.

Informe obrigatoriamente:

- **Serviço/Aplicação**: o que será monitorado
- **Tipo de monitoramento**: disponibilidade, performance, logs, métricas
- **Métricas**: especifique as métricas desejadas (CPU, memória, latência, etc)
- **Thresholds**: limites para disparo de alertas
- **Canais de notificação**: Slack, e-mail, PagerDuty
- **Severidade do alerta**: Info, Warning, Critical

📊 Dashboards podem ser solicitados junto com o monitoramento.''',
            'form_fields': [
                {'name': 'servico', 'type': 'text', 'label': 'Serviço/Aplicação', 'required': True},
                {'name': 'tipo_monitoramento', 'type': 'select', 'label': 'Tipo de Monitoramento', 'options': ['Disponibilidade', 'Performance', 'Logs', 'Métricas'], 'required': True},
                {'name': 'metricas', 'type': 'textarea', 'label': 'Métricas Desejadas', 'required': True},
                {'name': 'thresholds', 'type': 'textarea', 'label': 'Thresholds para Alertas', 'required': True},
                {'name': 'canais_notificacao', 'type': 'textarea', 'label': 'Canais de Notificação', 'required': True}
            ]
        },
        {
            'name': 'Solicitação de Novo Repositório',
            'template': '''Utilize este tópico para **solicitar a criação de um novo repositório** no GitHub da organização.
Para que a solicitação seja processada corretamente, preencha todas as informações abaixo:

- **Dados gerais do repositório**:
    - Nome sugerido para o repositório (exemplo: `minha-api-backend`)
    - Breve descrição do projeto, que será utilizada no **README**
    - Squad ou time responsável pela manutenção do repositório
- **Configurações do repositório**:
    - Defina a **visibilidade**:
        - Privado
        - Internal (uso interno da empresa)
        - Público (requer aprovação prévia)
    - Informe a **linguagem principal**, utilizada para geração automática do `.gitignore`
    - Indique se o repositório deve ser criado a partir de um **template** existente e, em caso positivo, qual template deve ser utilizado
- **Acessos iniciais**:
    - Informe quais **times ou usuários** devem possuir **permissão de escrita (Write)** no repositório
    - Caso necessário, indique a **liberação de acesso ao Grafana** relacionada a este repositório

⚠️ Solicitações sem informações completas ou sem definição de responsáveis poderão ser devolvidas para correção.''',
            'form_fields': [
                {'name': 'nome_repositorio', 'type': 'text', 'label': 'Nome do Repositório', 'required': True},
                {'name': 'descricao', 'type': 'textarea', 'label': 'Descrição do Projeto', 'required': True},
                {'name': 'squad_responsavel', 'type': 'text', 'label': 'Squad/Time Responsável', 'required': True},
                {'name': 'visibilidade', 'type': 'select', 'label': 'Visibilidade', 'options': ['Privado', 'Internal', 'Público'], 'required': True},
                {'name': 'linguagem_principal', 'type': 'text', 'label': 'Linguagem Principal', 'required': True},
                {'name': 'template', 'type': 'text', 'label': 'Template (se aplicável)', 'required': False},
                {'name': 'times_acesso', 'type': 'textarea', 'label': 'Times/Usuários com Acesso Write', 'required': True},
                {'name': 'acesso_grafana', 'type': 'select', 'label': 'Liberar Acesso Grafana?', 'options': ['Sim', 'Não'], 'required': False}
            ]
        },
        {
            'name': 'Reporte de Indisponibilidade',
            'template': '''Utilize este tópico para **reportar indisponibilidades, falhas ou degradação de serviços e/ou projetos**.
Para agilizar a análise e resolução do incidente, preencha as informações abaixo com o máximo de detalhes possível:

- **Serviço afetado**:
    - Nome do sistema ou serviço impactado
    - URL (link) onde o erro está ocorrendo
    - Ambiente afetado: **Produção**, **Homologação/Staging**, **Desenvolvimento (Dev)** ou outro, se aplicável
- **Sintomas observados**:
    - Descreva o que está acontecendo, como por exemplo:
        - Site não carrega
        - Lentidão extrema
        - Erros 404 ou 500
        - Funcionalidade quebrada
        - Outro comportamento inesperado
    - Informe a **mensagem de erro exibida**, caso exista
- **Impacto do incidente**:
    - Indique quem está sendo afetado:
        - Apenas você
        - Vários usuários
        - Todos os usuários (parada total)
    - Informe desde quando o problema ocorre, com **horário aproximado**

⚠️ Quanto mais detalhadas forem as informações, mais rápido será o diagnóstico e a resolução do incidente.''',
            'form_fields': [
                {'name': 'nome_servico', 'type': 'text', 'label': 'Nome do Serviço/Sistema', 'required': True},
                {'name': 'url_erro', 'type': 'text', 'label': 'URL do Erro', 'required': True},
                {'name': 'ambiente', 'type': 'select', 'label': 'Ambiente Afetado', 'options': ['Produção', 'Homologação/Staging', 'Desenvolvimento', 'Outro'], 'required': True},
                {'name': 'sintomas', 'type': 'select', 'label': 'Sintoma Principal', 'options': ['Site não carrega', 'Lentidão extrema', 'Erro 404', 'Erro 500', 'Funcionalidade quebrada', 'Outro'], 'required': True},
                {'name': 'descricao_sintomas', 'type': 'textarea', 'label': 'Descrição Detalhada dos Sintomas', 'required': True},
                {'name': 'mensagem_erro', 'type': 'textarea', 'label': 'Mensagem de Erro (se exibida)', 'required': False},
                {'name': 'impacto', 'type': 'select', 'label': 'Impacto', 'options': ['Apenas eu', 'Vários usuários', 'Todos os usuários (parada total)'], 'required': True},
                {'name': 'horario_inicio', 'type': 'datetime', 'label': 'Horário Aproximado do Início', 'required': True}
            ]
        }
    ]
    
    count_created = 0
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            name=topic_data['name'],
            defaults={
                'template': topic_data['template'],
                'form_fields': topic_data['form_fields']
            }
        )
        if created:
            print(f"Topic created: {topic_data['name']}")
            count_created += 1
        else:
            print(f"Topic already exists: {topic_data['name']}")

    print(f"\nPopulação concluída! {count_created} tópicos criados.")

if __name__ == '__main__':
    populate()
