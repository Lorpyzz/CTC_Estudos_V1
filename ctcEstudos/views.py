import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from ctcEstudos.models import User, Disciplina, Turma, SessaoEstudo, Professor, InscricaoTurma
from ctcEstudos.forms import AlunoForm, DisciplinaForm, TurmaForm, SessaoEstudoForm, InscricaoTurmaForm, TopicoForm

def paginaInicial(request):
    return render(request, "home.html")

def loginAluno(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                nome_exibicao = user.nome if user.nome else user.username
                messages.success(request, f"Bem-vindo de volta, {nome_exibicao}!")
                return redirect("disciplinas") 
            
        messages.error(request, "Erro: Matrícula e/ou senha incorretos.")
        
    else:
        form = AuthenticationForm()
        
    if 'username' in form.fields:
        form.fields['username'].label = 'Matrícula'
        form.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Matrícula'
        })
    if 'password' in form.fields:
        form.fields['password'].label = 'Senha'
        form.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Senha'
        })
        
    return render(request, 'form_login.html', {'form': form})


def paginaCadastro(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.matricula
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect("disciplinas.html")
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')
    else:
        form = AlunoForm()
    alunos = User.objects.all()
    return render(request, "form_aluno.html", {"form": form, "alunos": alunos})


def paginaDisciplinas(request):
    if request.method == "POST":
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina criada com sucesso!')
            return redirect('disciplinas')
    else:
        disciplina = Disciplina.objects.all()
        form = DisciplinaForm()
    return render(request, "disciplinas.html", context={"disciplina": disciplina, "form": form})

def paginaTurmas(request):
    if request.user.is_authenticated:
        inscricoes = InscricaoTurma.objects.filter(user=request.user).select_related('turma__disciplina', 'turma__professor')
    else:
        inscricoes = []
    return render(request, "turmas.html", {"inscricoes": inscricoes})

def paginaFlashcards(request):
    return render(request, "flashcards.html")

def paginaDuvidas(request):
    return render(request, "duvidas.html")

def paginaChat(request):
    return render(request, "chat.html")

def paginaDisciplinaDetalhe(request, nome):
    return render(request, f"{nome}.html")


def form_disciplina(request):
    if request.method == "POST":
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')
    else:
        form = DisciplinaForm()
    return render(request, "form_disciplina.html", {"form": form})

def form_turma(request):
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')
    else:
        form = TurmaForm()
    return render(request, "form_turma.html", {"form": form})

def form_sessao_estudo(request):
    if request.method == "POST":
        form = SessaoEstudoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')
    else:
        form = SessaoEstudoForm()
    return render(request, "form_sessao_estudo.html", {"form": form})

def form_inscricao(request):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para se inscrever em uma turma.")
        
        return redirect('loginAluno') 

    if request.method == "POST":
        
        form = InscricaoTurmaForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.user = request.user  
            inscricao.save()
            messages.success(request, 'Inscrição realizada com sucesso!')
            return redirect('turmas')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')
    else:
        form = InscricaoTurmaForm()

    turmas = Turma.objects.select_related('disciplina').all()
    mapping = {}
    for t in turmas:
        disc_id = t.disciplina.id
        if disc_id not in mapping:
            mapping[disc_id] = []
        if t.codigo_turma not in mapping[disc_id]:
            mapping[disc_id].append(t.codigo_turma)
            
    mapping_json = json.dumps(mapping)
    return render(request, "form_inscricao.html", {"form": form, "mapping_json": mapping_json})

def form_topico(request):
    if request.method == "POST":
        form = TopicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')
    else:
        form = TopicoForm()
    return render(request, "form_topico.html", {"form": form})