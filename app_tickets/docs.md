# Documentação do App: Tickets (`app_tickets`)

## Visão Geral
O `app_tickets` é o módulo operacional do sistema. Ele gerencia o ciclo de vida das solicitações (tickets), desde a abertura até a resolução, incluindo comunicação e arquivos.

## Modelos de Dados

### `Ticket`
- **Caminho**: `app_tickets.models.Ticket`
- **Descrição**: A unidade principal de trabalho. Representa uma solicitação única.
- **Estados (Status Workflow)**:
    - `OPEN`: Aberto (Padrão).
    - `ACCEPTED`: Aceito (Triagem realizada).
    - `IN_PROGRESS`: Em andamento (DevOps atuando).
    - `BLOCKED`: Travado (Impedimento externo).
    - `DONE`: Finalizado.
- **Campos Principais**:
    - `title`, `description`: Dados da solicitação.
    - `requester` (FK User): Quem pediu.
    - `assignee` (FK User): Quem está atendendo (DevOps).
    - `project` (FK Project): Projeto relacionado.
    - `topic` (FK Topic): Categoria.
    - `status`: Estado atual.

### `TicketAttachment` (Anexo)
- **Caminho**: `app_tickets.models.TicketAttachment`
- **Descrição**: Arquivos de suporte (logs, imagens) ligados a um ticket.

### `Comment` (Comentário)
- **Caminho**: `app_tickets.models.Comment`
- **Descrição**: Mensagens trocadas dentro do ticket.
- **Funcionalidade**:
    - `is_internal`: Se marcado como `True`, o comentário é visível apenas para a equipe de Staff, permitindo discussão técnica interna sem poluir a visão do solicitante.

## Funcionalidades e Views

### Portal de Tickets
- **Meus Tickets**: Lista filtrada para o usuário comum ver suas demandas.
- **Fila de Atendimento**: Lista completa para a equipe DevOps.

### Detalhes do Ticket
- Visualização completa do status e dados.
- **Timeline**: Exibição cronológica de comentários.
- **Interação**: Formulário para adicionar novos comentários.
- **Gestão**: Para Staff, opções para assumir o ticket, mudar status ou editar.

### Notificações
- O sistema dispara e-mails automáticos (template `ticket_created.html`) para notificar sobre a abertura de novos chamados, utilizando um layout simplificado e direto.
