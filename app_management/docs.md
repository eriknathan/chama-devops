# Documentação do App: Gerenciamento (`app_management`)

## Visão Geral
O `app_management` é o núcleo administrativo do ChamaDevOps. Ele gerencia as entidades organizacionais fundamentais (Projetos e Tópicos) e provê a interface principal de navegação (Dashboard).

## Modelos de Dados

### `Project` (Projeto)
- **Caminho**: `app_management.models.Project`
- **Descrição**: Representa um projeto de software, produto ou iniciativa que demandará suporte de DevOps.
- **Campos**:
    - `name` (CharField): Nome do projeto.
    - `description` (TextField): Detalhes sobre o escopo do projeto (opcional).
    - `manager` (ForeignKey -> User): O gerente ou responsável principal pelo projeto (opcional).
    - `members` (ManyToManyField -> User): Equipe de desenvolvedores associada ao projeto.
    - `created_at`, `updated_at`: Carimbos de tempo automáticos.

### `Topic` (Tópico)
- **Caminho**: `app_management.models.Topic`
- **Descrição**: Categorias para classificação de tickets. Exemplos: "Infraestrutura", "Banco de Dados", "CI/CD".
- **Campos**:
    - `name` (CharField): Nome do tópico.

## Funcionalidades e Views

### Dashboard (`/management/dashboard/`)
- Painel principal do sistema.
- Exibe métricas rápidas: Quantidade de tickets abertos, em andamento, finalizados.
- Lista os tickets mais recentes.
- Adapta a visualização com base no perfil do usuário (Staff vê tudo, User vê apenas seus tickets).

### Gestão de Projetos (`/management/projects/`)
- **Listagem**: Tabela com projetos cadastrados, exibindo nome, gerente e data.
    - Ações rápidas via ícones: Visualizar, Editar, Excluir.
- **Detalhes**: Página exclusiva com informações completas do projeto, incluindo descrição formatada e lista de membros com iniciais.
- **CRUD**: Formulários completos para criar e editar projetos, incluindo seleção de gerente e membros.

### Gestão de Tópicos (`/management/topics/`)
- CRUD simples para manutenção das categorias de chamados. Apenas usuários Staff têm acesso.
