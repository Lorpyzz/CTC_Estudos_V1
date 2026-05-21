import os
import re

base_dir = r'CTC_Estudos_V1'

# 1. Update views.py
views_path = os.path.join(base_dir, 'ctcEstudos', 'views.py')
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

views_content = re.sub(r'(?m)^\s*#.*$', '', views_content)


if 'from django.contrib import messages' not in views_content:
    views_content = views_content.replace('from django.shortcuts import render, redirect', 'from django.shortcuts import render, redirect\nfrom django.contrib import messages')


for form_name in ['DisciplinaForm', 'TurmaForm', 'SessaoEstudoForm', 'InscricaoTurmaForm', 'TopicoForm', 'AlunoForm']:
    pattern = rf"""(form = {form_name}\(request\.POST\)\s+if form\.is_valid\(\):\s+form\.save\(\))(\s+return redirect\('[^']+'\))"""
    replacement = rf"\1\n            messages.success(request, 'Cadastro realizado com sucesso!')\2"
    views_content = re.sub(pattern, replacement, views_content)

    pattern_else = rf"""(form = {form_name}\(request\.POST\)\s+if form\.is_valid\(\):[\s\S]+?return redirect\('[^']+'\))"""
    replacement_else = rf"\1\n        else:\n            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')"
    views_content = re.sub(pattern_else, replacement_else, views_content)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)


forms_path = os.path.join(base_dir, 'ctcEstudos', 'forms.py')
with open(forms_path, 'r', encoding='utf-8') as f:
    forms_content = f.read()

forms_content = forms_content.replace("""        if not disciplina:
            disciplina = Disciplina.objects.filter(nome__iexact=val).first()
            
            if not (disciplina.is_valid()):
                raise forms.ValidationError("Disciplina inválida.")""", """        if not disciplina:
            disciplina = Disciplina.objects.filter(nome__iexact=val).first()
            if not disciplina:
                raise forms.ValidationError("Disciplina não encontrada com esse código/nome.")""")

validation_code = """

    def clean(self):
        cleaned_data = super().clean()
        concluida = cleaned_data.get('concluida')
        nota_final = cleaned_data.get('nota_final')
        if concluida and (nota_final is None or nota_final < 5.0):
            raise forms.ValidationError("Para marcar como concluída, a nota final deve ser informada e maior ou igual a 5.0.")
        return cleaned_data"""
if 'def clean(self):' not in forms_content.split('class InscricaoTurmaForm')[1].split('class TopicoForm')[0]:
    forms_content = forms_content.replace("        }", "        }" + validation_code, 1) # Insert in InscricaoTurmaForm


forms_content = re.sub(r'(?m)^\s*#.*$', '', forms_content)

with open(forms_path, 'w', encoding='utf-8') as f:
    f.write(forms_content)


emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
messages_html = """
        {% if messages %}
        <div style="margin-bottom: 20px;">
            {% for message in messages %}
            <div style="padding: 10px; border-radius: 5px; {% if message.tags == 'error' %}background-color: #f8d7da; color: #721c24;{% else %}background-color: #d4edda; color: #155724;{% endif %}">
                {{ message }}
            </div>
            {% endfor %}
        </div>
        {% endif %}
"""

for filename in os.listdir(base_dir):
    if filename.startswith('form_') and filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()

        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

        if '{% if messages %}' not in html_content:
            html_content = html_content.replace('<section class="form-card">', f'<section class="form-card">{messages_html}')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

print("Done")
