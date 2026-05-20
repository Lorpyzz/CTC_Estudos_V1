from django.shortcuts import render, redirect
from views.cadastro import usuarios

ADMIN_MOCK = {
    "matricula": "admin2025",
    "senha": "ctcadmin@puc",
}

def login(request):
    erro = None

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        matricula = request.POST.get("matricula", "").strip()
        senha = request.POST.get("senha", "")

        if tipo == "aluno":
            usuario = None
            for u in usuarios:
                if (u['matricula'] == matricula and u['senha'] == senha):
                    usuario = u
                    break

            if usuario:
                return redirect("home")
            else:
                erro = "Matrícula ou senha inválidos."

        elif tipo == "admin":
            if matricula == ADMIN_MOCK["matricula"] and senha == ADMIN_MOCK["senha"]:
                return redirect("home")
            else:
                erro = "Credenciais de administrador inválidas."

    return render(request, "login.html", {"erro": erro})