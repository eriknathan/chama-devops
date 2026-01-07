
import re
from django.utils.text import slugify

def parse_markdown_to_dict(text):
    """
    Parses a markdown string extracting key-value pairs formatted as **Key**: Value.
    Keys are normalized to snake_case (slugified with underscores).
    """
    data = {}
    if not text:
        return data
        
    lines = text.split('\n')
    current_key = None
    accumulated_value = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Match **Header**: Value
        match = re.match(r'\*\*(.+?)\*\*:\s*(.*)', line)
        if match:
            # Save previous
            if current_key:
                val = '\n'.join(accumulated_value).strip()
                data[current_key] = val
            
            raw_key = match.group(1).strip()
            # Normalize key: "Nome Completo" -> "nome_completo"
            key = slugify(raw_key).replace('-', '_')
            
            value = match.group(2).strip()
            
            current_key = key
            accumulated_value = [value] if value else []
        else:
            # Check for headers or separators which stop the current field
            if line.startswith('###') or line.startswith('---'):
                if current_key:
                    val = '\n'.join(accumulated_value).strip()
                    data[current_key] = val
                    current_key = None
                    accumulated_value = []
                continue
                
            if current_key:
                 accumulated_value.append(line)
                 
    if current_key:
        data[current_key] = '\n'.join(accumulated_value).strip()
        
    return data
