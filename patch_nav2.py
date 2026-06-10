import os
import glob
import re

html_files = glob.glob('c:/Users/amorzinho/CTC_Estudos_V1/*.html') + glob.glob('c:/Users/amorzinho/CTC_Estudos_V1/Gabriel/*.html')

for file_path in html_files:
    if "turmas.html" in file_path:
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where <a href="/disciplinas/">...</a> is, inside a <li>, and insert the turmas <li> after it.
    # Pattern looks for the closing </li> of the disciplinas link.
    # We want to match: <li>...<a href="/disciplinas/">...</a>...</li>
    # and we want to ensure we don't insert it if it's already there.
    
    if 'href="/turmas/"' in content:
        continue
        
    pattern = re.compile(r'(<li>\s*<a href="/disciplinas/">.*?</a>\s*</li>)', re.IGNORECASE | re.DOTALL)
    
    def replacer(match):
        return match.group(1) + '\n            <li><a href="/turmas/">Minhas Turmas</a></li>'
    
    new_content = pattern.sub(replacer, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {file_path}")
