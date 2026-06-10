from django.db import models
from django.conf import settings


class Chat(models.Model):

    usuario1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats_usuario1'
    )

    usuario2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats_usuario2'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.usuario1} x {self.usuario2}"


class Mensagem(models.Model):

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='mensagens'
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    conteudo = models.TextField()

    enviado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['enviado_em']

    def __str__(self):
        return f"{self.usuario.username}: {self.conteudo[:20]}"from django.db import models
from django.conf import settings


class Chat(models.Model):

    # PRIMEIRO USUARIO DO CHAT
    usuario1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats_usuario1'
    )

    # SEGUNDO USUARIO DO CHAT
    usuario2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats_usuario2'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.usuario1} x {self.usuario2}"


class Mensagem(models.Model):

    # CHAT AO QUAL A MENSAGEM PERTENCE
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='mensagens'
    )

    # USUARIO QUE ENVIOU
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # CONTEUDO DA MENSAGEM
    conteudo = models.TextField()

    # DATA/HORA DA MENSAGEM
    enviado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['enviado_em']

    def __str__(self):

        return f"{self.usuario.username}: {self.conteudo[:20]}"