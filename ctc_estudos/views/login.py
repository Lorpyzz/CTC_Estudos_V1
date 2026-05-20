from django.shortcuts import render, redirect

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
            return redirect("home")

        elif tipo == "admin":
            if matricula == ADMIN_MOCK["matricula"] and senha == ADMIN_MOCK["senha"]:
                return redirect("home")
            else:
                erro = "Credenciais de administrador inválidas."

    return render(request, "login.html", {"erro": erro})