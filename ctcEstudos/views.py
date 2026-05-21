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
        return redirect("home.html")

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo de volta, {user.nome}!")
                return redirect("disciplinas.html") 
            
        messages.error(request, "Erro: E-mail ou senha incorretos, ou usuário não possui cadastro.")
        
    else:
        form = AuthenticationForm()
        
    return render(request, 'forms_login.html', {'form': form})


def paginaCadastro(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
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
    else:
        disciplina = Disciplina.objects.all()
        form = DisciplinaForm()
    return render(request, "disciplinas.html", context={"disciplina": disciplina})

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
    if request.method == "POST":
        form = InscricaoTurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos informados.')
    else:
        form = InscricaoTurmaForm()
    return render(request, "form_inscricao.html", {"form": form})

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
