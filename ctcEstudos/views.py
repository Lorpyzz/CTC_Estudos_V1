from django.shortcuts import render

# Create your views here.

def paginaInicial(request):
    return render(request, "home.html")

def paginaCadastro(request, email = None, password = None):
    # Renderiza o template específico para React
    return render(request, "react_index.html")

def paginaDisciplinas(request):
    # Renderiza a página HTML pura em vez do React
    return render(request, "disciplinas.html")

def paginaFlashcards(request):
    return render(request, "flashcards.html")

def paginaDuvidas(request):
    return render(request, "duvidas.html")

def paginaChat(request):
    return render(request, "chat.html")

def paginaDisciplinaDetalhe(request, nome):
    # Renderiza o arquivo HTML correspondente (Django procura nas pastas configuradas)
    return render(request, f"{nome}.html")