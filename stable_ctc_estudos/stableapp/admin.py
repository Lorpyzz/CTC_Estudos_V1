from django.contrib import admin
from .models import (
    CtcEstudosUser, Professor, Disciplina, Turma, InscricaoTurma,
    Topico, Conteudo, Monitoria, SessaoEstudo, Chat, Mensagem,
    PerguntaFrequente, Duvida, RespostaDuvida, Deck, Flashcard
)

# Register your models here.

admin.site.register(CtcEstudosUser)
admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(InscricaoTurma)
admin.site.register(Topico)
admin.site.register(Conteudo)
admin.site.register(Monitoria)
admin.site.register(SessaoEstudo)
admin.site.register(Chat)
admin.site.register(Mensagem)
admin.site.register(PerguntaFrequente)
admin.site.register(Duvida)
admin.site.register(RespostaDuvida)
admin.site.register(Deck)
admin.site.register(Flashcard)