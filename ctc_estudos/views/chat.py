from django.shortcuts import render, redirect

from chat.models import Chat, Mensagem


def chat_view(request):

    # PEGA O PRIMEIRO CHAT
    chat = Chat.objects.first()

    # SE NÃO EXISTIR CHAT, CRIA UM
    if not chat:

        chat = Chat.objects.create(
            usuario1=request.user,
            usuario2=request.user
        )

    # ENVIO DE MENSAGEM
    if request.method == "POST":

        texto = request.POST.get("mensagem")

        if texto:

            Mensagem.objects.create(
                chat=chat,
                usuario=request.user,
                conteudo=texto
            )

        return redirect('chat')

    # PEGA TODAS AS MENSAGENS
    mensagens = chat.mensagens.all()

    return render(
        request,
        "chat.html",
        {
            "mensagens": mensagens,
            "chat": chat
        }
    )