import os
import re

def fix_templates(root_dir):
    print(f"Scanning {root_dir}...")
    count = 0
    # simple way to match django tags, non-greedy
    # Note: This regex assumes tags don't nest (which they don't in Django)
    # and handles multi-line by using re.DOTALL implicitly via loop or just matching pattern
    # Actually, best to iterate matches.
    
    tag_pattern = re.compile(r'(\{%.*?%\})', re.DOTALL)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue
                
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            
            def replace_tag(match):
                tag_content = match.group(1)
                
                # 1. Remove newlines and collapse whitespace
                # Replace newlines with space
                tag_content = tag_content.replace('\n', ' ')
                # Collapse multiple spaces to single space
                tag_content = re.sub(r'\s+', ' ', tag_content)
                
                # 2. Fix == spacing
                # Replace any spacing around == with exactly ' == '
                tag_content = re.sub(r'\s*==\s*', ' == ', tag_content)
                
                return tag_content

            new_content = tag_pattern.sub(replace_tag, content)

            if new_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    print(f"Fixed: {filepath}")
                    count += 1
    
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    fix_templates('templates')
