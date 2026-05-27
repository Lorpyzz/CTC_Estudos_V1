from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

import json

from .models import (
    Disciplina,
    Turma,
    SessaoEstudo,
    InscricaoTurma,
    Chat,
    Mensagem
)

from .forms import (
    AlunoForm,
    DisciplinaForm,
    TurmaForm,
    SessaoEstudoForm,
    InscricaoTurmaForm,
    TopicoForm
)

# PEGA O MODEL CUSTOMIZADO
User = get_user_model()


def paginaInicial(request):
    return render(request, "home.html")


# =========================================
# LOGIN
# =========================================

def loginAluno(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get(
                'username'
            )

            password = form.cleaned_data.get(
                'password'
            )

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                nome_exibicao = (
                    user.nome
                    if user.nome
                    else user.username
                )

                messages.success(
                    request,
                    f"Bem-vindo de volta, {nome_exibicao}!"
                )

                return redirect("disciplinas")

        messages.error(
            request,
            "Erro: Matrícula e/ou senha incorretos."
        )

    else:
        form = AuthenticationForm()

    # CUSTOMIZA CAMPOS
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

    return render(
        request,
        'form_login.html',
        {'form': form}
    )


# =========================================
# CADASTRO
# =========================================

def paginaCadastro(request):

    if request.method == "POST":

        form = AlunoForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # LOGIN COM MATRICULA
            user.username = user.matricula

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            messages.success(
                request,
                'Cadastro realizado com sucesso!'
            )

            return redirect("disciplinas")

        else:

            messages.error(
                request,
                'Erro no cadastro.'
            )

    else:
        form = AlunoForm()

    alunos = User.objects.all()

    return render(
        request,
        "form_aluno.html",
        {
            "form": form,
            "alunos": alunos
        }
    )


# =========================================
# DISCIPLINAS
# =========================================

def paginaDisciplinas(request):

    if request.method == "POST":

        form = DisciplinaForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Disciplina criada com sucesso!'
            )

            return redirect('disciplinas')

    else:
        form = DisciplinaForm()

    disciplinas = Disciplina.objects.all()

    return render(
        request,
        "disciplinas.html",
        {
            "disciplinas": disciplinas,
            "form": form
        }
    )


# =========================================
# TURMAS
# =========================================

@login_required
def paginaTurmas(request):

    inscricoes = (
        InscricaoTurma.objects
        .filter(user=request.user)
        .select_related(
            'turma__disciplina',
            'turma__professor'
        )
    )

    return render(
        request,
        "turmas.html",
        {"inscricoes": inscricoes}
    )


# =========================================
# FLASHCARDS
# =========================================

def paginaFlashcards(request):

    disciplinas = Disciplina.objects.all()

    return render(
        request,
        "flashcards.html",
        {"disciplinas": disciplinas}
    )


# =========================================
# DUVIDAS
# =========================================

def paginaDuvidas(request):

    disciplinas = Disciplina.objects.all()

    return render(
        request,
        "duvidas.html",
        {"disciplinas": disciplinas}
    )


# =========================================
# CHAT
# =========================================

@login_required
def paginaChat(request):

    usuario = request.user

    chat_obj = Chat.objects.first()

    if not chat_obj:

        chat_obj = Chat.objects.create(
            usuario1=usuario,
            usuario2=usuario
        )

    if request.method == "POST":

        texto = request.POST.get("mensagem")

        if texto:

            Mensagem.objects.create(
                chat=chat_obj,
                usuario=usuario,
                conteudo=texto
            )

        return redirect("chat")

    mensagens = (
        chat_obj.mensagens.all()
    )

    return render(
        request,
        "chat.html",
        {
            "mensagens": mensagens
        }
    )

# =========================================
# DETALHE DISCIPLINA
# =========================================

def paginaDisciplinaDetalhe(
    request,
    nome
):

    return render(
        request,
        f"{nome}.html"
    )


# =========================================
# FORM DISCIPLINA
# =========================================

def form_disciplina(request):

    if request.method == "POST":

        form = DisciplinaForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Cadastro realizado com sucesso!'
            )

            return redirect('disciplinas')

        else:

            messages.error(
                request,
                'Erro no cadastro.'
            )

    else:
        form = DisciplinaForm()

    return render(
        request,
        "form_disciplina.html",
        {"form": form}
    )


# =========================================
# FORM TURMA
# =========================================

def form_turma(request):

    if request.method == "POST":

        form = TurmaForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Cadastro realizado com sucesso!'
            )

            return redirect('disciplinas')

        else:

            messages.error(
                request,
                'Erro no cadastro.'
            )

    else:
        form = TurmaForm()

    return render(
        request,
        "form_turma.html",
        {"form": form}
    )


# =========================================
# FORM SESSAO ESTUDO
# =========================================

@login_required
def form_sessao_estudo(request):

    if request.method == "POST":

        form = SessaoEstudoForm(request.POST)

        if form.is_valid():

            sessao = form.save(commit=False)

            sessao.aluno = request.user

            sessao.save()

            messages.success(
                request,
                'Sessão cadastrada!'
            )

            return redirect('disciplinas')

    else:
        form = SessaoEstudoForm()

    return render(
        request,
        "form_sessao_estudo.html",
        {"form": form}
    )


# =========================================
# INSCRICAO
# =========================================

@login_required
def form_inscricao(request):

    if request.method == "POST":

        form = InscricaoTurmaForm(
            request.POST
        )

        if form.is_valid():

            inscricao = form.save(
                commit=False
            )

            inscricao.user = request.user

            inscricao.save()

            messages.success(
                request,
                'Inscrição realizada!'
            )

            return redirect('turmas')

        else:

            messages.error(
                request,
                'Erro no cadastro.'
            )

    else:
        form = InscricaoTurmaForm()

    turmas = (
        Turma.objects
        .select_related('disciplina')
        .all()
    )

    mapping = {}

    for t in turmas:

        disc_id = t.disciplina.id

        if disc_id not in mapping:
            mapping[disc_id] = []

        if t.codigo_turma not in mapping[disc_id]:

            mapping[disc_id].append(
                t.codigo_turma
            )

    mapping_json = json.dumps(mapping)

    return render(
        request,
        "form_inscricao.html",
        {
            "form": form,
            "mapping_json": mapping_json
        }
    )


# =========================================
# FORM TOPICO
# =========================================

def form_topico(request):

    if request.method == "POST":

        form = TopicoForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Cadastro realizado!'
            )

            return redirect('disciplinas')

        else:

            messages.error(
                request,
                'Erro no cadastro.'
            )

    else:
        form = TopicoForm()

    return render(
        request,
        "form_topico.html",
        {"form": form}
    )