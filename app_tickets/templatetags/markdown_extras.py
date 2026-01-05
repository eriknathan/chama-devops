import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.filter(name='render_markdown')
def render_markdown(text):
    """
    Renderiza markdown básico para HTML com layout de cards para campos chave: valor.
    """
    if not text:
        return ''
    
    # Escape HTML first for security
    text = escape(text)
    
    lines = text.split('\n')
    html_parts = []
    current_section = None
    fields = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for header (### Header)
        header_match = re.match(r'^###\s*(.+)$', line)
        if header_match:
            # If we have accumulated fields, output them first
            if fields:
                html_parts.append(_render_fields_grid(fields))
                fields = []
            current_section = header_match.group(1)
            html_parts.append(f'<h3 class="text-lg font-bold text-foreground mb-4 flex items-center gap-2"><svg class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>{current_section}</h3>')
            continue
        
        # Check for **Label**: Value pattern
        field_match = re.match(r'^\*\*(.+?)\*\*:\s*(.*)$', line)
        if field_match:
            label = field_match.group(1)
            value = field_match.group(2).strip() or '<span class="text-muted-foreground italic">Não informado</span>'
            
            # Detect and convert URLs to links
            if value and 'http' in value:
                value = re.sub(
                    r'(https?://[^\s<]+)',
                    r'<a href="\1" target="_blank" class="text-primary hover:underline break-all">\1</a>',
                    value
                )
            
            fields.append({'label': label, 'value': value})
            continue
        
        # Regular text
        if line:
            if fields:
                html_parts.append(_render_fields_grid(fields))
                fields = []
            html_parts.append(f'<p class="text-muted-foreground mb-2">{line}</p>')
    
    # Output remaining fields
    if fields:
        html_parts.append(_render_fields_grid(fields))
    
    return mark_safe('\n'.join(html_parts))


def _render_fields_grid(fields):
    """Renderiza os campos em um grid de cards."""
    html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">'
    
    for field in fields:
        label = field['label']
        value = field['value']
        
        # Add icon based on field name
        icon = _get_field_icon(label)
        
        html += f'''
        <div class="bg-muted/30 rounded-lg p-4 border border-border/50">
            <div class="flex items-center gap-2 mb-1">
                {icon}
                <span class="text-xs font-medium text-muted-foreground uppercase tracking-wide">{label}</span>
            </div>
            <div class="text-sm font-medium text-foreground">{value}</div>
        </div>
        '''
    
    html += '</div>'
    return html


def _get_field_icon(label):
    """Retorna um ícone SVG baseado no nome do campo."""
    label_lower = label.lower()
    
    if 'email' in label_lower:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>'
    elif 'nome' in label_lower or 'name' in label_lower or 'usuário' in label_lower or 'user' in label_lower:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>'
    elif 'link' in label_lower or 'url' in label_lower or 'repositório' in label_lower:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>'
    elif 'permissão' in label_lower or 'acesso' in label_lower or 'nível' in label_lower:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" /></svg>'
    elif 'tipo' in label_lower or 'solicitação' in label_lower:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>'
    elif 'motivo' in label_lower or 'justificativa' in label_lower or 'descrição' in label_lower:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" /></svg>'
    elif 'github' in label_lower:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'
    else:
        return '<svg class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'


@register.filter(name='strip_markdown')
def strip_markdown(text):
    """
    Remove sintaxe markdown e retorna texto limpo para preview.
    """
    if not text:
        return ''
    
    # Remove headers (###, ##, #)
    text = re.sub(r'^#{1,3}\s*', '', text, flags=re.MULTILINE)
    
    # Remove bold (**text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    
    # Remove italic (*text*)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


@register.filter(name='extract_first_value')
def extract_first_value(text):
    """
    Extrai o primeiro valor de campo (ex: **Label**: Value -> Value)
    para usar como preview mais significativo.
    """
    if not text:
        return ''
    
    # Remove headers
    text = re.sub(r'^#{1,3}\s*[^\n]+\n?', '', text, flags=re.MULTILINE)
    
    # Find first **Label**: Value pattern
    match = re.search(r'\*\*(.+?)\*\*:\s*(.+?)(?:\*\*|$)', text)
    if match:
        label = match.group(1)
        value = match.group(2).strip()
        if value:
            return f"{label}: {value}"
    
    # Fallback to stripped markdown
    return strip_markdown(text)[:100]
