from django.contrib import admin
from .models import User, Professor, Disciplina, Turma, InscricaoTurma, Topico, Conteudo, Monitoria, SessaoEstudo

# Register your models here.

admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(InscricaoTurma)
admin.site.register(Topico)
admin.site.register(Conteudo)
admin.site.register(Monitoria)
admin.site.register(SessaoEstudo)
