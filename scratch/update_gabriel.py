import os
import re

directory = r'\CTC_Estudos_V1\Gabriel'

replacements = [
    (r'href\s*=\s*"disciplinas\.css"', 'href="{% static \'disciplinas.css\' %}"'),
    (r'href\s*=\s*"programacao\.css"', 'href="{% static \'programacao.css\' %}"'),
    (r'src\s*=\s*"site-logo\.png"', 'src="{% static \'site-logo.png\' %}"'),
    (r'src\s*=\s*"ctc-logo\.png"', 'src="{% static \'ctc-logo.png\' %}"'),
    (r'src\s*=\s*"puc-rio-logo\.png"', 'src="{% static \'puc-rio-logo.png\' %}"'),
    (r'href\s*=\s*"index\.html"', 'href="/"'),
    (r'href\s*=\s*"disciplinas\.html"', 'href="/disciplinas/"'),
    (r'href\s*=\s*"flashcards\.html"', 'href="/flashcards/"'),
    (r'href\s*=\s*"duvidas\.html"', 'href="/duvidas/"'),
    (r'href\s*=\s*"chat\.html"', 'href="/chat/"'),
    (r'href\s*=\s*""\s*class\s*=\s*"btn"', 'href="/cadastro/" class="btn"'),
    (r"onclick=\"document\.location='disciplinas\.html'\"", "onclick=\"document.location='/disciplinas/'\"")
]

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add load static if not present
        if '{% load static %}' not in content:
            content = '{% load static %}\n' + content
        
        # Apply replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Gabriel files updated successfully.")
