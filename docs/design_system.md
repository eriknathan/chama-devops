# Design System

O **ChamaDevOps** utiliza uma identidade visual "Clean Professional", implementada com **TailwindCSS**.

## Cores Principais

| Nome      | Cor Tailwind   | Uso Principal               |
|-----------|----------------|-----------------------------|
| **Primary** | `indigo-600`   | Botões de ação, Links, Highlights |
| **Secondary**| `purple-600`   | Detalhes, Gradients         |
| **Background**| `slate-50`     | Fundo da aplicação          |
| **Surface**   | `white`        | Cards, Modais, Paineis      |
| **Text Main** | `slate-900`    | Títulos e textos fortes     |
| **Text Body** | `slate-600`    | Texto padrão de leitura     |

## Status Badges (Tickets)

Cores semânticas para identificar o estado dos chamados:

*   🟡 **Aberto**: `yellow-100` (bg) / `yellow-800` (text)
*   🔵 **Aceito**: `blue-100` / `blue-800`
*   ⚙️ **Em Andamento**: `indigo-100` / `indigo-800`
*   🔴 **Travado**: `red-100` / `red-800`
*   🟢 **Finalizado**: `emerald-100` / `emerald-800`

## Componentes Comuns

### Cards
Utilizados para listar itens (Projetos, Tickets em mobile).
*   **Estilo**: `bg-white rounded-xl shadow-sm border border-slate-100`
*   **Hover**: `hover:shadow-md transition-shadow`

### Botões Primários
*   **Estilo**: `bg-indigo-600 text-white rounded-lg shadow-sm hover:bg-indigo-700`
*   **Foco**: `focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`

### Tabelas (Desktop)
Utilizadas em telas administrativas.
*   **Header**: `bg-slate-50 text-slate-500 uppercase text-xs font-medium`
*   **Linhas**: `divide-y divide-slate-200`
*   **Responsividade**: Envolvidas em `overflow-x-auto` para não quebrar em telas menores.

## Tipografia
Fonte padrão: **Inter** (Google Fonts).
*   Prioriza legibilidade com bom espaçamento (`tracking-tight` em títulos, `leading-relaxed` em textos).
