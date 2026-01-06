# Visão Geral do Projeto

**ChamaDevOps** é uma plataforma centralizada para gerenciamento de solicitações de DevOps.

## Objetivo
O principal objetivo é eliminar a comunicação descentralizada (Slack, E-mail, Corredor) e garantir visibilidade, rastreabilidade e organização para as demandas de infraestrutura e suporte técnico.

## Fluxo Principal de Uso

O sistema atende a dois perfis principais de usuário:

1.  **Solicitante (Usuário Comum)**
    *   Acessa o Dashboard para ver seus tickets.
    *   Abre novos chamados preenchendo o formulário com templates pré-definidos.
    *   Define a prioridade do chamado (Baixa, Média, Alta, Crítica).
    *   Acompanha o status e interage através de comentários.
    *   Visualiza o histórico de alterações do ticket.

2.  **DevOps (Staff/Admin)**
    *   Visualiza a fila geral de tickets de todos os projetos.
    *   Filtra tickets por prioridade, status e projeto.
    *   Acessa o **Dashboard de Relatórios** para visualizar métricas, evolução de abertura de chamados e produtividade.
    *   Realiza a triagem (Aceitar/Atribuir tickets).
    *   Trabalha na resolução e atualiza o status (Em Andamento -> Finalizado).
    *   Utiliza comentários internos para documentação técnica.
    *   Acompanha métricas de SLA (tempo de primeira resposta e resolução).

## Requisitos do Sistema

### Requisitos Funcionais (RF)

*   **RF01 - Autenticação**: O sistema deve permitir login e logout de usuários via e-mail e senha.
*   **RF02 - Gestão de Projetos**: Administradores podem criar, editar e visualizar projetos, atribuindo gerentes e membros.
*   **RF03 - Gestão de Tópicos**: Administradores podem criar categorias (tópicos) com templates e campos dinâmicos.
*   **RF04 - Abertura de Tickets**: Usuários autenticados podem abrir chamados informando título, descrição, projeto, tópico, prioridade e anexos.
*   **RF05 - Gestão de Tickets**: A equipe DevOps pode visualizar todos os tickets, alterar status, atribuir responsáveis e filtrar por critérios.
*   **RF06 - Comentários**: Possibilidade de adicionar comentários nos tickets. A equipe DevOps pode criar *comentários internos* (invisíveis ao solicitante).
*   **RF07 - Dashboard**: Painel visual com métricas de tickets abertos, fechados e evolução mensal.
*   **RF08 - Prioridade de Tickets**: Tickets devem ter níveis de prioridade (Baixa, Média, Alta, Crítica) para triagem adequada.
*   **RF09 - Histórico de Mudanças**: Todas as alterações de status e responsável devem ser registradas para auditoria.
*   **RF10 - Métricas SLA**: O sistema deve registrar tempo de primeira resposta e tempo de resolução.
*   **RF11 - Templates de Tópicos**: Tópicos podem ter modelos pré-definidos com campos dinâmicos para padronizar solicitações.
*   **RF12 - Download de PDF**: Possibilidade de exportar detalhes do ticket em formato PDF.

### Requisitos Não Funcionais (RNF)

*   **RNF01 - Responsividade**: A interface deve ser adaptável a dispositivos móveis (Mobile First) e desktops.
*   **RNF02 - Segurança**: Acesso administrativo restrito a usuários com flag `is_staff`.
*   **RNF03 - Armazenamento**: Upload de arquivos deve ser suportado, com armazenamento via MinIO (compatível S3).
*   **RNF04 - Performance**: O carregamento das páginas principais não deve exceder 2 segundos em conexões estáveis.
*   **RNF05 - Containerização**: O sistema deve rodar em containers Docker para facilitar deploy e escalabilidade.

## Ciclo de Vida do Ticket

Um ticket passa pelos seguintes estados:

1.  **OPEN (Aberto)**: Estado inicial ao ser criado.
2.  **ACCEPTED (Aceito)**: Triagem realizada, ticket reconhecido pela equipe.
3.  **IN_PROGRESS (Em Andamento)**: Trabalho técnico sendo executado.
4.  **BLOCKED (Travado)**: Aguardando terceiros ou informações adicionais.
5.  **DONE (Finalizado)**: Solicitação concluída com sucesso.

## Níveis de Prioridade

Os tickets podem ter as seguintes prioridades:

| Prioridade | Descrição | Cor |
|------------|-----------|-----|
| 🟢 **Baixa (LOW)** | Solicitações sem urgência | Verde |
| 🔵 **Média (MEDIUM)** | Prioridade padrão | Azul |
| 🟠 **Alta (HIGH)** | Requer atenção prioritária | Laranja |
| 🔴 **Crítica (CRITICAL)** | Urgente, impacto em produção | Vermelho |

Para visualizar o fluxo detalhado, consulte a documentação de [Arquitetura](arquitetura.md) ou os diagramas no [PRD](prd.md).
