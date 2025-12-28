# Fluxos de Uso

Este documento ilustra os principais fluxos de navegação e interação dos usuários com o sistema ChamaDevOps.

## Fluxo Principal (Solicitante e DevOps)

O diagrama abaixo detalha a jornada desde o login até a resolução de um ticket, diferenciando as ações de usuários comuns (Solicitantes) e da equipe técnica (DevOps).

```mermaid
graph TD
    %% User Entry
    A[Visitante] -->|Acessa Sistema| B(Login Page)
    B -->|Credenciais Inválidas| B
    B -->|Sucesso| C{Perfil do Usuário}

    %% Solicitante Flow
    C -- Solicitante --> D[Dashboard User]
    D --> E[Novo Ticket]
    D --> F[Meus Tickets]
    E -->|Preenche Dados| K[Formulário]
    K -->|Salvar| L[Ticket Criado]
    
    %% Ticket Lifecycle - Interaction
    L -->|Notificação| M(DevOps Team)
    F -->|Visualizar| N[Detalhes do Ticket]
    N -->|Novo Comentário| O[Discussão]

    %% DevOps Flow
    C -- DevOps --> G[Dashboard Admin]
    G --> I[Fila de Tickets]
    I -->|Seleciona Ticket| P[Triagem]
    
    %% DevOps Actions
    P -->|Aceitar/Atribuir| Q[Status: Accepted]
    Q -->|Trabalhar| R[Status: In Progress]
    R -->|Resolver| S[Status: Done]
    
    %% Feedback Loop
    S -->|Notificação| T(Solicitante)
    R -->|Comentário Interno/Externo| O
    O -->|Notificação| M
```
