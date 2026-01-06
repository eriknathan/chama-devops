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
    E -->|Seleciona Tópico| E1[Template Carrega]
    E1 -->|Define Prioridade| E2[Formulário Dinâmico]
    E2 -->|Anexa Arquivos| E3[Upload]
    E3 -->|Salvar| L[Ticket Criado]
    
    %% Ticket Lifecycle - Interaction
    L -->|Notificação| M(DevOps Team)
    F -->|Visualizar| N[Detalhes do Ticket]
    N -->|Ver Histórico| N1[Timeline de Mudanças]
    N -->|Novo Comentário| O[Discussão]
    N -->|Download| N2[Exportar PDF]

    %% DevOps Flow
    C -- DevOps --> G[Dashboard Admin]
    G --> H[Relatórios/Métricas]
    G --> I[Fila de Tickets]
    I -->|Filtrar| I1[Por Prioridade/Status]
    I1 -->|Seleciona Ticket| P[Triagem]
    
    %% DevOps Actions
    P -->|Aceitar/Atribuir| Q[Status: Accepted]
    Q -->|Trabalhar| R[Status: In Progress]
    R -->|Bloquear| R1[Status: Blocked]
    R1 -->|Desbloquear| R
    R -->|Resolver| S[Status: Done]
    
    %% Feedback Loop
    S -->|Notificação| T(Solicitante)
    R -->|Comentário Interno| O1[Nota Interna]
    R -->|Comentário Externo| O
    O -->|Notificação| M
```

---

## Fluxo de Criação de Ticket

Detalhamento do processo de abertura de um novo ticket pelo solicitante.

```mermaid
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant D as DevOps

    U->>S: Clica em "Novo Ticket"
    S->>U: Exibe formulário
    U->>S: Seleciona Projeto
    U->>S: Seleciona Tópico
    S->>U: Carrega Template do Tópico
    U->>U: Preenche campos dinâmicos
    U->>S: Define Prioridade
    U->>S: Anexa arquivos (opcional)
    U->>S: Salvar Ticket
    S->>S: Cria registro no banco
    S->>S: Registra histórico inicial
    S->>D: Notificação de novo ticket
    S->>U: Redireciona para detalhes
```

---

## Fluxo de Triagem (DevOps)

Processo de aceitação e atribuição de tickets pela equipe DevOps.

```mermaid
stateDiagram-v2
    [*] --> OPEN: Ticket Criado
    OPEN --> ACCEPTED: DevOps Aceita
    ACCEPTED --> IN_PROGRESS: Inicia Trabalho
    IN_PROGRESS --> BLOCKED: Aguardando Info
    BLOCKED --> IN_PROGRESS: Info Recebida
    IN_PROGRESS --> DONE: Resolve
    DONE --> [*]
    
    note right of OPEN: Prioridade define ordem na fila
    note right of ACCEPTED: Registrado em TicketHistory
    note right of DONE: Métricas SLA calculadas
```

---

## Fluxo de SLA e Métricas

O sistema registra automaticamente métricas para análise de performance.

```mermaid
timeline
    title Ciclo de Vida do Ticket com SLA
    
    section Criação
        Ticket Aberto : created_at registrado
        
    section Primeira Resposta
        DevOps Aceita : first_response_at registrado
        SLA de Resposta : Tempo calculado
        
    section Resolução
        Ticket Finalizado : resolved_at registrado
        SLA de Resolução : Tempo total calculado
```

---

## Legenda de Perfis

| Perfil | Permissões | Identificação |
|--------|------------|---------------|
| **Solicitante** | Ver próprios tickets, criar tickets, comentar | `is_staff = False` |
| **DevOps** | Ver todos os tickets, triagem, comentários internos, relatórios | `is_staff = True` |
| **Admin** | Todas as acima + gestão de projetos, tópicos e usuários | `is_superuser = True` |
