# Arquitetura do Sistema

O ChamaDevOps segue uma arquitetura **Monólito Modular** baseada no framework Django 6.0.

## Stack Tecnológica

*   **Backend**: Python 3.12+ / Django 6.0
*   **Frontend**: Django Templates + TailwindCSS (via CDN para desenvolvimento rápido)
*   **Banco de Dados**: SQLite (Desenvolvimento) / PostgreSQL (Produção - Recomendado)

## Estrutura de Diretórios

A organização do código segue a separação por domínios (`apps`) com o prefixo `app_`.

```text
chama-devops/
├── core/                   # Configurações do Projeto (settings, urls, wsgi)
├── app_accounts/           # Gestão de Identidade (User Model, Auth)
├── app_management/         # Domínio Administrativo (Projetos, Tópicos)
├── app_tickets/            # Domínio Operacional (Tickets, Comentários)
├── templates/              # Templates HTML globais e por app
├── static/                 # Arquivos estáticos (CSS, JS, Imagens)
├── docs/                   # Documentação do projeto
└── manage.py               # Utilitário de comando do Django
```

### Detalhes dos Módulos

#### 1. `app_accounts`
Responsável pela autenticação e autorização.
*   Implementa um **Custom User Model** (`User`) que utiliza `email` como identificador principal (sem `username`).
*   Gerencia o login, logout e permissões básicas (`is_staff`).

#### 2. `app_management`
Responsável pelas estruturas organizacionais.
*   **Project**: Grupos lógicos de tickets (ex: "Migração AWS", "Suporte Interno").
*   **Topic**: Categorias de tickets (ex: "Infra", "Acesso", "CI/CD").

#### 3. `app_tickets`
O núcleo operacional do sistema.
*   **Ticket**: A solicitação em si. Conecta Users, Projects e Topics.
*   **Comment**: Comunicação dentro do ticket. Suporta comentários internos (apenas staff).
*   **TicketAttachment**: Arquivos anexados aos tickets.

## Decisões de Design

*   **Responsividade**: Interface construída com TailwindCSS "mobile-first", garantindo acesso em celulares e desktops.
*   **Simplicidade**: Uso de templates server-side para evitar complexidade de SPA (Single Page Applications) desnecessária.
