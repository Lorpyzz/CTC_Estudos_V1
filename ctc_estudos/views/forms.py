from django.shortcuts import render, redirect
from views.disciplinas import disciplinas_lista

def forms(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        codigo = request.POST.get("codigo")
        descricao = request.POST.get("descricao")
        departamento = request.POST.get("departamento")

        nova_disciplina = {
            "id": len(disciplinas_lista) + 1,
            "nome": nome,
            "codigo": codigo,
            "descricao": descricao,
            "departamento": departamento,
        }

        disciplinas_lista.append(nova_disciplina)
        return redirect("lista_disciplinas")

    return render(request, "forms.html")