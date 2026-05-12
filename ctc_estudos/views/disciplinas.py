import json
from django.shortcuts import render


def lista_disciplinas(request):

    dados_json = """
    {
      "disciplinas": [
        {
          "id": 1,
          "nome": "Programação",
          "descricao": "Ponteiros, alocação dinâmica, arquivos, estruturas e introdução a estruturas de dados em C."
        },
        {
          "id": 2,
          "nome": "Estruturas de Dados",
          "descricao": "Listas, pilhas, filas, árvores, grafos e análise de complexidade."
        },
        {
          "id": 3,
          "nome": "Estruturas de Dados Avançadas",
          "descricao": "Árvores balanceadas, tabelas hash, heaps e algoritmos de ordenação avançados."
        },
        {
          "id": 4,
          "nome": "Cálculo I",
          "descricao": "Limites, derivadas, integrais e aplicações de funções de uma variável."
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