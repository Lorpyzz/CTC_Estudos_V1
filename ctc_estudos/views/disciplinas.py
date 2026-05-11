import json
from django.shortcuts import render


def lista_disciplinas(request):

    dados_json = """
    {
      "disciplinas": [
        {
          "id": 1,
          "nome": "Matemática",
          "descricao": "Estudo de álgebra, geometria e cálculo."
        },
        {
          "id": 2,
          "nome": "História",
          "descricao": "Estudo dos acontecimentos históricos mundiais."
        },
        {
          "id": 3,
          "nome": "Física",
          "descricao": "Estudo das leis da natureza e do universo."
        },
        {
          "id": 4,
          "nome": "Programação",
          "descricao": "Introdução ao desenvolvimento de software."
        },
        {
          "id": 5,
          "nome": "Projetos",
          "descricao": "Matéria legal de projetos."
        }
      ]
    }
    """

    dados = json.loads(dados_json)

    disciplinas = dados["disciplinas"]

    context = {
        "disciplinas": disciplinas
    }

    return render(request, "disciplinas.html", context)