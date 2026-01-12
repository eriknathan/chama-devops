# Guia de Estilo para Templates Django

Este documento descreve as convenções de estilo aplicadas nos templates Django do projeto, especificamente nos arquivos de formulário em `templates/app_tickets/forms/`.

---

## 1. Tags Django em Linha Única

### Regra
Todas as template tags do Django (`{% ... %}`) devem estar em uma única linha, sem quebras de linha internas.

### ❌ Incorreto
```django
{% if sintoma_principal=='Site não carrega'
    %}selected{% endif %}
```

```django
{% if not object.priority or object.priority=='MEDIUM' %}selected{% endif
    %}
```

### ✅ Correto
```django
{% if sintoma_principal == 'Site não carrega' %}selected{% endif %}
```

```django
{% if not object.priority or object.priority == 'MEDIUM' %}selected{% endif %}
```

### Motivo
- **Legibilidade**: Tags em linha única são mais fáceis de ler e entender
- **Prevenção de erros**: Quebras de linha dentro de tags podem causar erros de sintaxe no Django template engine
- **Consistência**: Mantém um padrão uniforme em todo o projeto

---

## 2. Espaçamento em Operadores de Comparação

### Regra
O operador de igualdade (`==`) deve ter **um espaço antes e um espaço depois**.

### ❌ Incorreto
```django
{% if ambiente=='Produção' %}checked{% endif %}
```

```django
{% if object.priority=='HIGH' %}selected{% endif %}
```

### ✅ Correto
```django
{% if ambiente == 'Produção' %}checked{% endif %}
```

```django
{% if object.priority == 'HIGH' %}selected{% endif %}
```

### Motivo
- **Legibilidade**: Espaços tornam as comparações mais fáceis de identificar visualmente
- **Consistência com PEP 8**: Segue as convenções do Python para espaçamento em operadores
- **Manutenibilidade**: Código mais limpo facilita revisões e manutenção

---

## Comandos Utilizados para Correção

### Correção de quebras de linha em template tags
```bash
python3 -c "
import re
import os

forms_dir = 'templates/app_tickets/forms'

for filename in os.listdir(forms_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(forms_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        def fix_multiline_tag(match):
            tag = match.group(0)
            fixed = re.sub(r'\s*\n\s*', ' ', tag)
            fixed = re.sub(r'\s+', ' ', fixed)
            return fixed
        
        pattern = r'\{%[^%]*?\n[^%]*?%\}'
        new_content = content
        while re.search(pattern, new_content):
            new_content = re.sub(pattern, fix_multiline_tag, new_content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
"
```

### Correção de espaçamento em operadores `==`
```bash
sed -i '' "s/==/ == /g" templates/app_tickets/forms/*.html
```

---
