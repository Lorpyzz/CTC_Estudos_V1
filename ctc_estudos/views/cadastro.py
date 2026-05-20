from django.shortcuts import render, redirect

# "banco" mockado — fica em memória enquanto o servidor estiver rodando
usuarios = []

def cadastro(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # verifica se as senhas coincidem
        if senha != confirmar_senha:
            return render(request, 'cadastro.html', {'erro': 'As senhas não coincidem.'})

        # verifica se a matrícula já está cadastrada
        if any(u['matricula'] == matricula for u in usuarios):
            return render(request, 'cadastro.html', {'erro': 'Matrícula já cadastrada.'})

        # salva o usuário no "banco"
        usuarios.append({'matricula': matricula, 'senha': senha})

        return redirect('login')  # redireciona para o login após cadastro

    return render(request, 'cadastro.html')