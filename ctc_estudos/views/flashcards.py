import json
from django.shortcuts import render

def flashcards(request):
    dados_json = """
    {
      "disciplinas": [
        {"id": 1, "nome": "Programação",                    "codigo": "INF1000"},
        {"id": 2, "nome": "Estruturas de Dados",            "codigo": "INF1010"},
        {"id": 3, "nome": "Estruturas de Dados Avançadas",  "codigo": "INF1100"},
        {"id": 4, "nome": "Cálculo I",                      "codigo": "MAT1000"},
        {"id": 5, "nome": "Cálculo II",                     "codigo": "MAT1110"}
      ]
    }
    """
    dados = json.loads(dados_json)
    disciplinas = dados["disciplinas"]
    return render(request, 'flashcards.html', {"disciplinas": disciplinas})