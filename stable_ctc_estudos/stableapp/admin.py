from django.contrib import admin
from .models import CtcEstudosUser, Professor, Disciplina, Turma, InscricaoTurma, Topico, Conteudo, Monitoria, SessaoEstudo

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
