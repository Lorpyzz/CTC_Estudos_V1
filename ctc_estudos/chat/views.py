from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from chat.models import Chat, Mensagem


def chat(request):

    chat_obj = Chat.objects.first()
    usuario = User.objects.first()

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

    mensagens = chat_obj.mensagens.all()

    return render(
        request,
        "chat.html",
        {"mensagens": mensagens}
    )