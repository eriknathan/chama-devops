# Banco de Dados

Este documento descreve detalhadamente a estrutura de dados ("Schema") do sistema ChamaDevOps.

## Diagrama ER (Entidade-Relacionamento)

```mermaid
erDiagram
    User ||--o{ Project : "gerencia (manager)"
    User ||--o{ Project : "membro_de (members)"
    User ||--o{ Ticket : "solicita (requester)"
    User ||--o{ Ticket : "atribuido_a (assignee)"
    User ||--o{ Comment : "autor_de"
    
    Project ||--o{ Ticket : "contem"
    Topic ||--o{ Ticket : "categoriza"
    
    Ticket ||--o{ Comment : "possui"
    Ticket ||--o{ TicketAttachment : "possui_arquivos"

    User {
        int id PK
        string email "Unique"
        string password
        string first_name
        string last_name
        bool is_staff
        bool is_active
        datetime date_joined
    }

    Project {
        int id PK
        string name
        text description
        int manager_id FK
        datetime created_at
        datetime updated_at
    }

    Topic {
        int id PK
        string name
        datetime created_at
        datetime updated_at
    }

    Ticket {
        int id PK
        string title
        text description
        string status
        int requester_id FK
        int assignee_id FK
        int project_id FK
        int topic_id FK
        datetime created_at
        datetime updated_at
    }
    
    Comment {
        int id PK
        text content
        bool is_internal
        int ticket_id FK
        int author_id FK
        datetime created_at
        datetime updated_at
    }

    TicketAttachment {
        int id PK
        string file "Path"
        int ticket_id FK
        datetime uploaded_at
    }
```

## Modelos Abstratos

### `BaseModel`
Modelo utilitário herdado pela maioria das entidades principais.
*   **created_at** (`DateTimeField`): Data de criação automática.
*   **updated_at** (`DateTimeField`): Data de atualização automática.

---

## Tabelas e Detalhes

### 1. Aplicação `app_accounts`

#### `User`
Tabela personalizada de usuários que substitui o padrão do Django.
*   **id** (`AutoField`): Chave primária.
*   **email** (`EmailField`): **Identificador Único** (Username removido).
*   **first_name** (`CharField`): Nome.
*   **last_name** (`CharField`): Sobrenome.
*   **is_staff** (`BooleanField`): Define se usuário é parte da equipe admin/DevOps.
*   **is_active** (`BooleanField`): Controle de conta ativa.

---

### 2. Aplicação `app_management`

#### `Project`
Representa um projeto, cliente ou contexto de trabalho.
*   **name** (`CharField`, max: 100): Nome do projeto.
*   **description** (`TextField`, opcional): Descrição detalhada.
*   **manager** (`ForeignKey` -> `User`): Gerente responsável (pode ser nulo).
    *   *Relacionamento*: Um usuário pode gerenciar N projetos.
*   **members** (`ManyToManyField` -> `User`): Lista de usuários vinculados ao projeto (ex: equipe).

#### `Topic`
Categorias transversais para organização.
*   **name** (`CharField`, max: 100): Nome do tópico (ex: "Infra", "Frontend").

---

### 3. Aplicação `app_tickets`

#### `Ticket`
A entidade central de solicitação.
*   **title** (`CharField`, max: 200): Resumo da demanda.
*   **description** (`TextField`): Detalhamento completo.
*   **status** (`CharField`, com choices):
    *   `OPEN`: Aberto
    *   `ACCEPTED`: Aceito
    *   `IN_PROGRESS`: Em Andamento
    *   `BLOCKED`: Travado
    *   `DONE`: Finalizado
*   **requester** (`ForeignKey` -> `User`): Quem abriu o chamado.
*   **assignee** (`ForeignKey` -> `User`, opcional): Quem está cuidando do chamado.
*   **project** (`ForeignKey` -> `Project`): Projeto de origem.
*   **topic** (`ForeignKey` -> `Topic`, opcional): Categoria da demanda.

#### `TicketAttachment`
Arquivos anexados a um ticket.
*   **ticket** (`ForeignKey` -> `Ticket`): Ticket pai.
*   **file** (`FileField`): Arquivo enviado (salvo em `media/app_tickets/`).
*   **uploaded_at** (`DateTimeField`): Data do envio.

#### `Comment`
Histórico de conversas dentro do ticket.
*   **ticket** (`ForeignKey` -> `Ticket`): Ticket pai.
*   **author** (`ForeignKey` -> `User`): Quem comentou.
*   **content** (`TextField`): Conteúdo da mensagem.
*   **is_internal** (`BooleanField`, padrão `False`): Se marcado, visível apenas para usuários `is_staff`.
