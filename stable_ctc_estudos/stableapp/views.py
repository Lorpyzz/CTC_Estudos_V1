from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.db.models import Q 
from django.db import IntegrityError  # ADICIONADO para capturar erro de duplicidade
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import PerguntaFrequente

import json

from .models import (
    Disciplina,
    Turma,
    SessaoEstudo,
    InscricaoTurma,
    Chat,
    Mensagem,
    Topico,
    Conteudo,
    Monitoria,
    Professor,
    Deck,
    Flashcard
)

from .forms import (
    AlunoForm,
    DisciplinaForm,
    TurmaForm,
    SessaoEstudoForm,
    InscricaoTurmaForm,
    TopicoForm,
    ConteudoForm,
    MonitoriaForm,
    ProfessorForm,
    DeckForm,
    FlashcardForm,
)

User = get_user_model()


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

                nome_exibicao = (
                    user.nome
                    if hasattr(user, 'nome') and user.nome
                    else user.username
                )

                messages.success(
                    request,
                    f"Bem-vindo de volta, {nome_exibicao}!"
                )
                return redirect("home")

        messages.error(
            request,
            "Erro: Matrícula e/ou senha incorretos."
        )
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

    return render(
        request,
        'form_login.html',
        {'form': form}
    )


def paginaCadastro(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.matricula
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(
                request,
                'Cadastro realizado com sucesso!'
            )
            return redirect("login")
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


def paginaDisciplinas(request):
    if request.method == "POST":
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Acesso negado: Apenas administradores podem criar disciplinas.")
            return redirect('disciplinas')
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


@login_required
def paginaTurmas(request):
    inscricoes = (
        InscricaoTurma.objects
        .filter(user=request.user, status__in=['ATIVA', 'CONCLUIDA'])
        .select_related(
            'turma__disciplina',
            'turma__professor'
        )
    )

    # CORREÇÃO: Alterado de 'topico__disciplina' para 'disciplina'
    sessoes = (
        SessaoEstudo.objects
        .filter(aluno=request.user)
        .select_related('disciplina')
        .order_by('-id')
    )

    return render(
        request,
        "turmas.html",
        {
            "inscricoes": inscricoes,
            "sessoes": sessoes
        }
    )


#FLASHCARDS--------------------
def paginaFlashcards(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deck criado com sucesso!')
            return redirect('flashcards')
        else:
            messages.error(request, 'Preencha a disciplina e o nome do deck.')

    decks = Deck.objects.select_related('disciplina').all()
    disciplinas = Disciplina.objects.all()
    return render(
        request,
        "flashcards.html",
        {"disciplinas": disciplinas, "decks": decks}
    )


def deck_detalhe(request, id):
    deck = get_object_or_404(Deck, id=id)
    cards = deck.cards.all()
    return render(
        request,
        "decks.html",
        {"deck": deck, "cards": cards}
    )


def delete_deck(request, id):
    deck = get_object_or_404(Deck, id=id)
    deck.delete()
    messages.success(request, 'Deck excluído.')
    return redirect('flashcards')


def criar_card(request, id):
    deck = get_object_or_404(Deck, id=id)
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            messages.success(request, 'Card adicionado!')
        else:
            messages.error(request, 'Preencha pergunta e resposta.')
    return redirect('deck_detalhe', id=deck.id)


def update_card(request, id):
    card = get_object_or_404(Flashcard, id=id)
    if request.method == "POST":
        form = FlashcardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card atualizado!')
        else:
            messages.error(request, 'Erro ao atualizar o card.')
    return redirect('deck_detalhe', id=card.deck.id)


def delete_card(request, id):
    card = get_object_or_404(Flashcard, id=id)
    deck_id = card.deck.id
    card.delete()
    messages.success(request, 'Card excluído.')
    return redirect('deck_detalhe', id=deck_id)
#-----------------------------


def paginaDuvidas(request):
    disciplinas = Disciplina.objects.all()
    return render(
        request,
        "duvidas.html",
        {"disciplinas": disciplinas}
    )


@login_required
def paginaChat(request):
    usuario = request.user

    disciplina_id = request.GET.get("disciplina") or request.POST.get("disciplina")
    disciplina_atual = None

    if disciplina_id:
        disciplina_atual = get_object_or_404(Disciplina, id=disciplina_id)

    pode_enviar = usuario.is_monitor or usuario.is_superuser

    if request.method == "POST":
        if not pode_enviar:
            messages.error(request, "Apenas monitores podem enviar mensagens.")
            if disciplina_id:
                return redirect(f"{reverse('chat')}?disciplina={disciplina_id}")
            return redirect("chat")

        texto = request.POST.get("mensagem", "").strip()
        if texto:
            Mensagem.objects.create(
                disciplina=disciplina_atual,  # None = Avisos Gerais
                usuario=usuario,
                conteudo=texto
            )

        if disciplina_id:
            return redirect(f"{reverse('chat')}?disciplina={disciplina_id}")
        return redirect("chat")

    # Busca mensagens filtradas por disciplina (ou avisos gerais se None)
    mensagens = Mensagem.objects.filter(
        disciplina=disciplina_atual
    ).select_related('usuario').order_by('enviado_em')

    disciplinas = Disciplina.objects.all()

    return render(request, "chat.html", {
    "mensagens": mensagens,
    "disciplinas": disciplinas,
    "disciplina_atual": disciplina_atual,
    "pode_enviar": pode_enviar,
})


def paginaDisciplinaDetalhe(request, nome):
    disciplina = None
    topicos = []
    turmas = []
    monitorias = []

    codigo = request.GET.get("codigo")

    if codigo:
        disciplina = Disciplina.objects.filter(
            codigo__iexact=codigo
        ).first()

        if disciplina:
            topicos = disciplina.topicos.all()
            turmas = (
                disciplina.turmas
                .select_related("professor")
                .all()
            )
            monitorias = (
                disciplina.monitorias_ativas
                .select_related("monitor")
                .all()
            )

    return render(
        request,
        "disciplina_detalhe.html",
        {
            "disciplina": disciplina,
            "topicos": topicos,
            "turmas": turmas,
            "monitorias": monitorias
        }
    )

@login_required
def form_disciplina(request):
    if request.method == "POST":
        if not request.user.is_superuser:
            messages.error(request, "Acesso negado: Apenas administradores podem acessar esta página.")
            return redirect('disciplinas')
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
        context={"form": form, "action": "Cadastrar"}
    )


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


@login_required
def form_sessao_estudo(request):
    if request.method == "POST":
        form = SessaoEstudoForm(request.POST, user=request.user)

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
        form = SessaoEstudoForm(user=request.user)

    return render(
        request,
        "form_sessao_estudo.html",
        {"form": form}
    )


@login_required
def form_inscricao(request):
    if request.method == "POST":
        form = InscricaoTurmaForm(request.POST)

        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.user = request.user

            # CORREÇÃO DE SEGURANÇA: Bloqueia duplicidade antes do insert
            ja_inscrito = InscricaoTurma.objects.filter(
                user=inscricao.user,
                turma=inscricao.turma
            ).exists()

            if ja_inscrito:
                messages.warning(
                    request, 
                    f"Você já possui uma inscrição ativa ou concluída na turma {inscricao.turma}!"
                )
                return redirect('turmas')

            try:
                inscricao.save()
                messages.success(request, 'Inscrição realizada!')
                return redirect('turmas')
            except IntegrityError:
                messages.error(request, 'Erro: Você já está matriculado nesta turma.')
                return redirect('turmas')
        else:
            messages.error(
                request,
                'Erro no cadastro.'
            )
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

    return render(
        request,
        "form_inscricao.html",
        {
            "form": form,
            "mapping_json": mapping_json
        }
    )


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


@login_required
def update_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    monitor_desta_disciplina = Monitoria.objects.filter(
        monitor=request.user, 
        disciplina=disciplina
    ).exists()

    if not monitor_desta_disciplina and not request.user.is_superuser:
        messages.error(request, 'Você não possui permissão para editar esta disciplina.')
        return redirect('disciplinas')
    
    if request.method == "POST":
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina updated com sucesso!')
            return redirect('disciplinas')
    else:
        form = DisciplinaForm(instance=disciplina)
        
    return render(request, "form_disciplina.html", context={"disciplina": disciplina, "form": form}) 


def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    
    ids_disciplinas_monitoradas = []
    if request.user.is_authenticated:
        ids_disciplinas_monitoradas = Monitoria.objects.filter(
            monitor=request.user
        ).values_list('disciplina_id', flat=True)

    context = {
        'disciplinas': disciplinas,
        'ids_disciplinas_monitoradas': ids_disciplinas_monitoradas,
    }
    return render(request, 'sua_lista.html', context)


@login_required
def delete_inscricao(request, turma_id):
    inscricao = get_object_or_404(
        InscricaoTurma,
        user=request.user,
        turma_id=turma_id
    )

    if inscricao.status == 'CONCLUIDA':
        messages.error(
            request,
            "Não é possível cancelar uma turma já concluída."
        )
        return redirect('turmas')

    inscricao.status = 'CANCELADA'
    inscricao.save()

    # CORREÇÃO: Alterado de 'topico__disciplina' para 'disciplina'
    SessaoEstudo.objects.filter(
        aluno=request.user,
        disciplina=inscricao.turma.disciplina
    ).delete()

    messages.success(
        request,
        "Inscrição cancelada com sucesso."
    )
    return redirect('turmas')


@login_required
def update_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = TurmaForm(instance=turma, user=request.user)
    
    if not request.user.is_monitor:
        return HttpResponseForbidden(
            "Você não tem permissão para alterar o professor."
        )
    return render(request, "form_turma.html", {"form": form, "turma": turma})


@login_required
def delete_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    
    is_enrolled = InscricaoTurma.objects.filter(
        user=request.user, 
        turma=turma, 
        status__in=['ATIVA', 'CONCLUIDA']
    ).exists()
    
    if not is_enrolled:
        messages.error(request, "Você só pode deletar uma turma na qual esteja matriculado.")
        return redirect('disciplinas')
        
    enrolled_users = InscricaoTurma.objects.filter(turma=turma).values_list('user', flat=True)
    
    # CORREÇÃO: Alterado de 'topico__disciplina' para 'disciplina'
    SessaoEstudo.objects.filter(
        aluno_id__in=enrolled_users, 
        disciplina=turma.disciplina
    ).delete()
    
    turma.delete()
    messages.success(request, "Turma deletada com sucesso.")
    return redirect('disciplinas')


def criar_sessao_estudo(request):
    if request.method == 'POST':
        form = SessaoEstudoForm(request.POST, user=request.user) 
        if form.is_valid():
            form.save()
            return redirect('alguma_url')
    else:
        form = SessaoEstudoForm(user=request.user) 
        
    return render(request, 'form_sessao_estudo.html', {'form': form})


@login_required
def update_sessao_estudo(request, id):
    sessao = get_object_or_404(SessaoEstudo, id=id, aluno=request.user)
    if request.method == "POST":
        form = SessaoEstudoForm(request.POST, instance=sessao, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sessão de estudo atualizada com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = SessaoEstudoForm(instance=sessao, user=request.user)
    return render(request, "form_sessao_estudo.html", {"form": form, "sessao": sessao})


@login_required
def delete_sessao_estudo(request, id):
    sessao = get_object_or_404(SessaoEstudo, id=id, aluno=request.user)
    sessao.delete()
    messages.success(request, 'Sessão de estudo deletada com sucesso!')
    return redirect('disciplinas')


@login_required
def update_inscricao(request, id):
    inscricao = get_object_or_404(InscricaoTurma, id=id, user=request.user)
    if request.method == "POST":
        form = InscricaoTurmaForm(request.POST, instance=inscricao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscrição atualizada com sucesso!')
            return redirect('turmas')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = InscricaoTurmaForm(instance=inscricao)
    return render(request, "form_inscricao.html", {"form": form, "inscricao": inscricao})


@login_required
def update_topico(request, id):
    topico = get_object_or_404(Topico, id=id)
    if request.method == "POST":
        form = TopicoForm(request.POST, instance=topico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tópico atualizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = TopicoForm(instance=topico)
    return render(request, "form_topico.html", {"form": form, "topico": topico})


@login_required
def delete_topico(request, id):
    topico = get_object_or_404(Topico, id=id)
    topico.delete()
    messages.success(request, 'Tópico deletado com sucesso!')
    return redirect('disciplinas')


@login_required
def form_conteudo(request):
    if request.method == "POST":
        form = ConteudoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conteúdo cadastrado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro no cadastro.')
    else:
        form = ConteudoForm()
    return render(request, "form_conteudo.html", {"form": form})


@login_required
def update_conteudo(request, id):
    conteudo = get_object_or_404(Conteudo, id=id)
    if request.method == "POST":
        form = ConteudoForm(request.POST, instance=conteudo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conteúdo atualizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = ConteudoForm(instance=conteudo)
    return render(request, "form_conteudo.html", {"form": form, "conteudo": conteudo})


@login_required
def delete_conteudo(request, id):
    conteudo = get_object_or_404(Conteudo, id=id)
    conteudo.delete()
    messages.success(request, 'Conteúdo deletado com sucesso!')
    return redirect('disciplinas')


@login_required
def form_monitoria(request):
    if request.method == "POST":
        dados_formulario = request.POST.copy()
        dados_formulario['monitor'] = request.user.id 
        
        form = MonitoriaForm(dados_formulario)

        if form.is_valid():
            monitoria = form.save(commit=False)
            monitoria.monitor = request.user
            monitoria.save()
            messages.success(request, 'Monitoria cadastrada com sucesso!')
            return redirect('monitoria')
        else:
            messages.error(request, 'Erro no cadastro.')
    else:
        form = MonitoriaForm(initial={'monitor': request.user})
    return render(request, "form_monitoria.html", {"form": form})


@login_required
def update_monitoria(request, id):
    monitoria = get_object_or_404(Monitoria, id=id)
    if request.method == "POST":
        form = MonitoriaForm(request.POST, instance=monitoria)
        if request.user.is_monitor:
            if form.is_valid():
                form.save()
                messages.success(request, 'Monitoria atualizada com sucesso!')
                return redirect('disciplinas')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = MonitoriaForm(instance=monitoria)
    return render(request, "form_monitoria.html", {"form": form, "monitoria": monitoria})


@login_required
def delete_monitoria(request):
    if request.user.is_monitor:
        monitoria = get_object_or_404(Monitoria, nome=request.user.nome)
        monitoria.delete()
        messages.success(request, 'Monitoria deletada com sucesso!')
    else:
        messages.error(request, 'Você não possui permissão para deletar uma monitoria.')
    return redirect('disciplinas')


@login_required
def exibe_monitoria(request):
    usuario_atual = request.user

    disciplinas_ids = InscricaoTurma.objects.filter(
        user=usuario_atual, 
        status='ATIVA'
    ).values_list('turma__disciplina_id', flat=True)

    monitorias_como_aluno = Monitoria.objects.filter(
        disciplina_id__in=disciplinas_ids
    ).exclude(monitor=usuario_atual).select_related('disciplina', 'monitor')

    monitorias_como_monitor = Monitoria.objects.filter(
        monitor=usuario_atual
    ).select_related('disciplina')

    return render(
        request,
        'monitoria.html',
        {
            'monitorias_aluno': monitorias_como_aluno,
            'monitorias_professor': monitorias_como_monitor,
        }
    )

@login_required
def form_professor(request):
    if request.method == "POST":
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor cadastrado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro no cadastro.')
    else:
        form = ProfessorForm()
    return render(request, "form_professor.html", {"form": form})


@login_required
def update_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    if request.method == "POST":
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor atualizado com sucesso!')
            return redirect('disciplinas')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, "form_professor.html", {"form": form, "professor": professor})


@login_required
def delete_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    professor.delete()
    messages.success(request, 'Professor deletado com sucesso!')
    return redirect('disciplinas')


@login_required
def update_aluno(request, id):
    if request.user.id != int(id):
        messages.error(request, "Você não tem permissão para editar este perfil.")
        return redirect('home')
    aluno = get_object_or_404(User, id=id)
    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro na atualização.')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, "form_aluno.html", {"form": form, "aluno": aluno})


@login_required
def delete_aluno(request, id):
    if request.user.id != int(id):
        messages.error(request, "Você não tem permissão para deletar este perfil.")
        return redirect('home')
    aluno = get_object_or_404(User, id=id)
    aluno.delete()
    messages.success(request, 'Perfil deletado com sucesso.')
    return redirect('home')


@login_required
def editar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)

    if not request.user.is_monitor:
        return HttpResponseForbidden(
            "Apenas monitores podem atualizar o professor."
        )

    form = TurmaForm(request.POST or None, instance=turma)

    if form.is_valid():
        form.save()
        return redirect('listar_turmas')

    return render(request, 'editar_turma.html', {'form': form})

def perfil(request):
    return render(request, 'perfil.html')

def ajuda(request):
    return render(request, 'ajuda.html')

def config(request):
    return render(request,'config.html')

def ajuda_view(request):
    perguntas = PerguntaFrequente.objects.all() 
    
    context = {
        'perguntas': perguntas
    }
    return render(request, 'ajuda.html', context)

def estudar_deck(request, id):
    deck = get_object_or_404(Deck, id=id)
    cards = list(deck.cards.values('id', 'pergunta', 'resposta'))
    return render(
        request,
        "estudo.html",
        {"deck": deck, "cards": cards}
    )