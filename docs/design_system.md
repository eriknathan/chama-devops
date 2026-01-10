# Design System (Flowlog)

## 🎨 Stack Visual

| Tecnologia        | Versão       | Descrição                              |
| ----------------- | ------------ | -------------------------------------- |
| **Tailwind CSS**  | v3.4         | Framework CSS utility-first (local)    |
| **PostCSS**       | v8.4         | Processador CSS                        |
| **Lucide**        | latest       | Biblioteca de ícones                   |
| **Alpine.js**     | v3.x         | Interatividade leve                    |
| **DM Sans**       | Google Fonts | Fonte principal (Moderna/Geometric)    |

---

## ⚙️ Tailwind CSS - Configuração Local

O Tailwind CSS é compilado localmente via um container Docker dedicado (`tailwind`) que observa mudanças nos arquivos `.html` e `.py` para gerar o CSS final.

### Arquivos de Configuração

| Arquivo | Descrição |
|---------|-----------|
| `tailwind.config.js` | Configuração de cores (Flowlog), fontes e tema |
| `static/src/input.css` | CSS fonte chaves variáveis HSL e `@imports` |
| `static/css/style.css` | CSS compilado (output) |

### Comandos de Build

```bash
# Monitorar mudanças e recompilar automaticamente (Watch Mode)
docker-compose up tailwind

# Ver logs do compilador
make css-logs

# Rebuild manual (se necessário)
docker-compose restart tailwind
```

---

## 🎯 Paleta de Cores (Flowlog)

O sistema utiliza cores HSL para fácil manipulação de opacidade.

### Modo Claro (`:root`)

|Token|HSL|Cor Hex (Aprox)|Uso|
|---|---|---|---|
|`--color-primary`|`251 100% 55%`|`#4318FF`|**Brand Purple** - Cor Principal|
|`--color-secondary`|`229 94% 70%`|`#6A82FB`|Azul Secundário|
|`--color-sidebar-bg`|`227 60% 17%`|`#111C44`|**Navy Dark** - Sidebar & Headers|
|`--text-main`|`231 46% 31%`|`#2B3674`|Texto Principal (Navy)|
|`--text-label`|`224 30% 73%`|`#A3AED0`|Texto Secundário (Cinza)|
|`--bg-body`|`222 67% 98%`|`#F4F7FE`|Fundo da Aplicação (Light Gray)|
|`--bg-surface`|`0 0% 100%`|`#FFFFFF`|Cards e Superfícies|

### Status Cores

|Token|HSL|Uso|
|---|---|---|
|`--status-success`|`166 95% 41%`|Verde (Done/Success)|
|`--status-warning`|`34 100% 64%`|Laranja/Amarelo (Warning)|
|`--status-error`|`5 83% 62%`|Vermelho (Error/Danger)|

---

## 🏷️ UI Components & Tokens

### Badges & Status

Os badges utilizam fundos com baixa opacidade e texto escuro para contraste.

| Status | Classes TailwindCSS |
|--------|---------------------|
| **Aberto** | `bg-indigo-50 text-indigo-600` |
| **Em Andamento** | `bg-orange-50 text-orange-600` |
| **Finalizado** | `bg-emerald-50 text-emerald-600` |
| **Travado** | `bg-red-50 text-red-600` |

### Cards "Clean Admin"

Os cards não utilizam bordas, apenas sombras suaves para profundidade.

```css
/* Shadow Soft Token */
--shadow-soft: 0px 18px 40px rgba(112, 144, 176, 0.12);
```

**Exemplo de Classe:**
`bg-white shadow-soft rounded-2xl`

### Botões

- **Primário:** `bg-brand text-white hover:bg-brand/90`
- **Raio de Borda:** `rounded-xl` (ou `16px`)

---

## 🔤 Tipografia

```css
font-family: 'DM Sans', sans-serif;
```

**Pesos utilizados:**
- **400 (Regular):** Texto corrido
- **500 (Medium):** Subtítulos e Labels
- **700 (Bold):** Títulos e Números Importantes

---

## ✅ Resumo da Identidade

- **Cor Principal:** Flowlog Purple (`#4318FF`)
- **Background:** Clean & Light (`#F4F7FE`)
- **Sidebar:** Navy Dark (`#111C44`) para contraste
- **Estilo:** Minimalista, "Clean Admin", sem excesso de bordas.
