import os
import glob

# Paths to search
html_files = glob.glob('c:/Users/amorzinho/CTC_Estudos_V1/*.html') + glob.glob('c:/Users/amorzinho/CTC_Estudos_V1/Gabriel/*.html')

target_str = """            <li>
                <a href="/disciplinas/">Disciplina</a>
            </li>
            <li>
                <a href="/flashcards/">Flashcards</a>
            </li>"""

replacement_str = """            <li>
                <a href="/disciplinas/">Disciplina</a>
            </li>
            <li>
                <a href="/turmas/">Minhas Turmas</a>
            </li>
            <li>
                <a href="/flashcards/">Flashcards</a>
            </li>"""

target_str_oneline = """            <li><a href="/disciplinas/">Disciplina</a></li>
            <li><a href="/flashcards/">Flashcards</a></li>"""
            
replacement_str_oneline = """            <li><a href="/disciplinas/">Disciplina</a></li>
            # <li><a href="/turmas/">Minhas Turmas</a></li>
            <li><a href="/flashcards/">Flashcards</a></li>"""

for file_path in html_files:
    if "turmas.html" in file_path or "flashcards.html" in file_path:
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    if target_str in content:
        content = content.replace(target_str, replacement_str)
        changed = True
    elif target_str_oneline in content:
        content = content.replace(target_str_oneline, replacement_str_oneline)
        changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {file_path}")
