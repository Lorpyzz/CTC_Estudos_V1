from django.shortcuts import render, redirect
from ctcEstudos.models import Aluno, Disciplina
from ctcEstudos.forms import AlunoForm

# Create your views here.

def paginaInicial(request):
    return render(request, "home.html")

def paginaCadastro(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        alunos = Aluno.objects.all()
        form = AlunoForm()
    return render(request, "forms.html", {"form": form, "alunos": alunos})


def paginaDisciplinas(request):
    disciplina = Disciplina.objects.all()
    return render(request, "disciplinas.html", context={"disciplina": disciplina})

def paginaFlashcards(request):
    return render(request, "flashcards.html")

def paginaDuvidas(request):
    return render(request, "duvidas.html")

def paginaChat(request):
    return render(request, "chat.html")

def paginaDisciplinaDetalhe(request, nome):
    
    return render(request, f"{nome}.html")


# def create_disciplina(request):
#     if request.method == "POST":
#         Disciplina.objects.create(
#             nome = request.POST['nome'],
#             codigo = request.POST['codigo'],
#             disciplina = request.POST['descricao'],
#             departamento = request.POST['departamento'],
#         )
#     return render(request, "")