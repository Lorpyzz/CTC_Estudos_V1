import json
from django.shortcuts import render, redirect
from datetime import datetime


def chat(request):
    mensagens = []
    try:
        with open("mensagens.json", "r", encoding="utf-8") as arquivo:
            mensagens = json.load(arquivo)
    except:
        mensagens = []


    if request.method == "POST":

        mensagem_usuario = request.POST.get("mensagem")

        nova_mensagem = {
            "usuario": "Isabele",
            "mensagem": mensagem_usuario,
            "horario": datetime.now().strftime("%H:%M")
        }
        mensagens.append(nova_mensagem)

        # salva json
        with open("mensagens.json", "w", encoding="utf-8") as arquivo:
            json.dump(
                mensagens,
                arquivo,
                ensure_ascii=False,
                indent=4
            )
        return redirect("chat")
    #envia variavel pro html
    return render(request, "chat.html", {"mensagens": mensagens})



