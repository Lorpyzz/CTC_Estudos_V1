import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctc_estudos.settings")
django.setup()

from ctcEstudos.forms import TurmaForm
from ctcEstudos.models import Disciplina, Professor

# Criar dados mock
d = Disciplina.objects.create(codigo="INF1000", nome="Teste", departamento="Informatica")
p = Professor.objects.create(nome="TESTE PROF", email="teste@puc.br", departamento="Informatica")

data = {
    'disciplina': 'INF1000',
    'professor': 'TESTE PROF',
    'codigo_turma': '33A',
    'semestre': '2026.1',
    'horario': 'segunda 11h'
}

form = TurmaForm(data)
if form.is_valid():
    print("VALID!")
    form.save()
else:
    print("INVALID!")
    print(form.errors)

d.delete()
p.delete()
