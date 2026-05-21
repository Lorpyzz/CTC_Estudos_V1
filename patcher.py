import os
import re

urls_path = r'CTC_Estudos_V1\ctc_estudos\urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    content = f.read()

urls_to_add = """    path('turmas/nova/', views.form_turma, name='form_turma'),
    path('sessoes/nova/', views.form_sessao_estudo, name='form_sessao_estudo'),
    path('inscricoes/nova/', views.form_inscricao, name='form_inscricao'),
    path('topicos/novo/', views.form_topico, name='form_topico'),
"""
if 'views.form_turma' not in content:
    content = content.replace("path('disciplinas/novo/', views.form_disciplina, name='form_disciplina'),",
                              "path('disciplinas/novo/', views.form_disciplina, name='form_disciplina'),\n" + urls_to_add)
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(content)

views_path = r'CTC_Estudos_V1\ctcEstudos\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

views_to_add = """
def form_disciplina(request):
    return render(request, "form_disciplina.html")

def form_turma(request):
    return render(request, "form_turma.html")

def form_sessao_estudo(request):
    return render(request, "form_sessao_estudo.html")

def form_inscricao(request):
    return render(request, "form_inscricao.html")

def form_topico(request):
    return render(request, "form_topico.html")
"""

if 'def form_disciplina' not in content:
    with open(views_path, 'a', encoding='utf-8') as f:
        f.write(views_to_add)

gabriel_dir = r'CTC_Estudos_V1\Gabriel'

btn_disciplinas_html = """                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px;">
                    <a href="{% url 'form_turma' %}" class="btn">Criar Turma</a>
                    <a href="{% url 'form_sessao_estudo' %}" class="btn">Criar Sessão de Estudo</a>
                    <a href="{% url 'form_disciplina' %}" class="btn">Criar Disciplina</a>
                    <a href="{% url 'form_inscricao' %}" class="btn">Inscrever-se em uma Turma</a>
                </div>"""

btn_topico_html = r'\1<a href="{% url \'form_topico\' %}" class="btn" style="margin: 10px 0; display: inline-block;">Adicionar um tópico</a>\n                \2'
btn_conteudo_html = r'\1\n        <div style="margin: 20px 0;"><input type="file" id="file_input" style="display: none;"><button class="btn" onclick="document.getElementById(\'file_input\').click()">Adicionar conteúdo</button></div>'

for file in os.listdir(gabriel_dir):
    if not file.endswith('.html'): continue
    filepath = os.path.join(gabriel_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if file == 'disciplinas.html':
        content = re.sub(r'<a href="\{% url \'form_disciplina\' %\}" class="btn">Cadastrar Disciplina</a>', btn_disciplinas_html, content)
    else:
        # Check if it's a discipline or topic
        is_topic = 'Voltar para materiais' in content
        is_discipline = ('Voltar para disciplinas' in content) and not is_topic

        if is_discipline:
            if 'Adicionar um tópico' not in content:
                # Insert after the <p> tag that follows <h1>
                content = re.sub(r'(<p>.*?</p>\s*)(<div class="col-1"></div>)', btn_topico_html, content, count=1, flags=re.DOTALL)
                # Fallback if the first replace doesn't work
                if 'Adicionar um tópico' not in content:
                     content = re.sub(r'(<p>.*?</p>)', r'\1\n                <a href="{% url \'form_topico\' %}" class="btn" style="margin: 10px 0; display: inline-block;">Adicionar um tópico</a>', content, count=1, flags=re.DOTALL)

        elif is_topic:
            if 'Adicionar conteúdo' not in content:
                # Insert after "Voltar para materiais" button
                content = re.sub(r'(<button class="btn1"[^>]*>.*?Voltar para materiais</button>\s*</div>?)', btn_conteudo_html, content, count=1, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done")
