# Design System

## 🎨 Stack Visual

| Tecnologia        | Versão       | Descrição                              |
| ----------------- | ------------ | -------------------------------------- |
| **Tailwind CSS**  | v3.x         | Framework CSS utility-first            |
| **shadcn/ui**     | -            | Componentes React baseados em Radix UI |
| **Framer Motion** | v12.x        | Animações e transições                 |
| **Lucide React**  | v0.462       | Biblioteca de ícones                   |
| **Inter**         | Google Fonts | Fonte principal                        |

---

## 🎯 Paleta de Cores (HSL)

### Modo Claro (`:root`)

|Token|HSL|Uso|
|---|---|---|
|`--background`|`0 0% 100%`|Fundo principal (branco)|
|`--foreground`|`222.2 84% 4.9%`|Texto principal (quase preto)|
|`--primary`|`24 95% 53%`|**AWS Orange** - Cor principal|
|`--secondary`|`220 14% 96%`|Superfícies secundárias|
|`--muted`|`220 14% 96%`|Elementos sutis|
|`--accent`|`24 95% 53%`|Destaques (igual primary)|
|`--destructive`|`0 84% 60%`|Ações destrutivas (vermelho)|
|`--border`|`220 13% 91%`|Bordas|

### Modo Escuro (`.dark`)

|Token|HSL|Uso|
|---|---|---|
|`--background`|`222 47% 6%`|Fundo escuro|
|`--foreground`|`210 40% 98%`|Texto claro|
|`--card`|`222 47% 9%`|Cards|
|`--secondary`|`222 47% 14%`|Superfícies secundárias|
|`--border`|`222 30% 18%`|Bordas escuras|

### Tokens AWS Customizados

|Token|HSL|Uso|
|---|---|---|
|`--aws-orange`|`24 95% 53%`|Laranja AWS principal|
|`--aws-orange-light`|`32 98% 60%`|Laranja claro|
|`--aws-dark`|`222 47% 11%`|Azul escuro AWS|
|`--aws-darker`|`222 47% 6%`|Azul mais escuro|
|`--success`|`142 76% 36%`|Verde sucesso|
|`--warning`|`38 92% 50%`|Amarelo warning|
|`--info`|`199 89% 48%`|Azul informativo|

---

## 🌈 Gradientes

```css
--gradient-primary: linear-gradient(135deg, hsl(24 95% 53%) -> hsl(32 98% 60%))
--gradient-dark: linear-gradient(180deg, hsl(222 47% 11%) -> hsl(222 47% 6%))
--gradient-card: linear-gradient(135deg, hsl(220 14% 98%) -> hsl(220 14% 96%))
```

---

## 🔲 Border Radius

|Token|Valor|
|---|---|
|`--radius`|`0.75rem` (12px)|
|`rounded-lg`|`0.75rem`|
|`rounded-md`|`0.5rem`|
|`rounded-sm`|`0.25rem`|

---

## 🔤 Tipografia

```css
font-family: 'Inter', system-ui, sans-serif;
```

**Pesos utilizados:** 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

---

## 💫 Animações

|Nome|Duração|Easing|Uso|
|---|---|---|---|
|`accordion-down/up`|0.2s|ease-out|Expandir/colapsar|
|`shimmer`|2s|infinite|Loading skeleton|
|`pulse`|2s|cubic-bezier|Destaque pulsante|
|`float`|3s|ease-in-out|Elementos flutuantes|
|`fadeIn`|0.5s|ease-out|Entrada suave|
|`slideUp`|0.5s|ease-out|Slide de baixo|
|`scaleIn`|0.3s|ease-out|Zoom de entrada|

---

## 🧩 Classes Utilitárias Customizadas

|Classe|Descrição|
|---|---|
|`.glass`|Efeito glassmorphism (blur + transparência)|
|`.gradient-text`|Texto com gradiente AWS|
|`.glow`|Sombra luminosa laranja|
|`.card-hover`|Hover com elevação + glow|
|`.animate-fade-in`|Animação de fade|
|`.animate-slide-up`|Animação slide up|
|`.animate-scale-in`|Animação scale|

---

## 🌙 Sombras

```css
--shadow-glow: 0 0 40px hsl(24 95% 53% / 0.15)    /* Glow laranja */
--shadow-card: 0 4px 24px -4px hsl(222 47% 11% / 0.1)  /* Sombra card */
shadow-glow-lg: 0 0 60px hsl(var(--aws-orange) / 0.25)  /* Glow maior */
```

---

## 📱 Breakpoints

|Nome|Largura|
|---|---|
|`sm`|640px|
|`md`|768px|
|`lg`|1024px|
|`xl`|1280px|
|`2xl`|1400px (container max)|

---

## ✅ Resumo da Identidade

- **Cor Principal:** AWS Orange (#F7931E em hex, `24 95% 53%` em HSL)
- **Modo Escuro:** Azul profundo AWS-inspired
- **Estilo:** Moderno, profissional, glassmorphism sutil
- **Transições:** Suaves (0.2s-0.5s), ease-out predominante
- **Acessibilidade:** Contraste adequado entre foreground/background
