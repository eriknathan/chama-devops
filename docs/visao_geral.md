# Visão Geral do Projeto

**ChamaDevOps** é uma plataforma centralizada para gerenciamento de solicitações de DevOps.

## Objetivo
O principal objetivo é eliminar a comunicação descentralizada (Slack, E-mail, Corredor) e garantir visibilidade, rastreabilidade e organização para as demandas de infraestrutura e suporte técnico.

## Fluxo Principal de Uso

O sistema atende a dois perfis principais de usuário:

1.  **Solicitante (Usuário Comum)**
    *   Acessa o Dashboard para ver seus tickets.
    *   Abre novos chamados preenchendo o formulário.
    *   Acompanha o status e interage através de comentários.

2.  **DevOps (Staff/Admin)**
    *   Visualiza a fila geral de tickets de todos os projetos.
    *   Realiza a triagem (Aceitar/Atribuir tickets).
    *   Trabalha na resolução e atualiza o status (Em Andamento -> Finalizado).
    *   Utiliza comentários internos para documentação técnica.

## Ciclo de Vida do Ticket

Um ticket passa pelos seguintes estados:

1.  **OPEN (Aberto)**: Estado inicial ao ser criado.
2.  **ACCEPTED (Aceito)**: Triagem realizada, ticket reconhecido pela equipe.
3.  **IN_PROGRESS (Em Andamento)**: Trabalho técnico sendo executado.
4.  **BLOCKED (Travado)**: Aguardando terceiros ou informações adicionais.
5.  **DONE (Finalizado)**: Solicitação concluída com sucesso.

Para visualizar o fluxo detalhado, consulte a documentação de [Arquitetura](arquitetura.md) ou os diagramas no PRD.
