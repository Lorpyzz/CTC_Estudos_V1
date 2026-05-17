import json
from django.shortcuts import render


def lista_disciplinas(request):

  dados_json = """
  {
    "disciplinas": [
      {
        "id": 1,
        "nome": "Programação",
        "descricao": "Ponteiros, alocação dinâmica, arquivos e estruturas em C."
      },
      {
        "id": 2,
        "nome": "Estruturas de Dados",
        "descricao": "Listas, pilhas, filas, árvores e grafos."
      },
      {
        "id": 3,
        "nome": "Estruturas Avançadas",
        "descricao": "Árvores balanceadas, heaps e tabelas hash."
      },
      {
        "id": 4,
        "nome": "Cálculo I",
        "descricao": "Limites, derivadas e integrais."
      },
      {
        "id": 5,
        "nome": "Cálculo II",
        "descricao": "Equações diferenciais e séries."
      },
      {
        "id": 6,
        "nome": "Física I",
        "descricao": "Cinemática, dinâmica, trabalho, energia e momento linear."
      },
      {
        "id": 7,
        "nome": "Física II",
        "descricao": "Gravitação, oscilações, ondas, termodinâmica e fluidos."
      },
      {
        "id": 8,
        "nome": "Programação Orientada a Objetos",
        "descricao": "Classes, herança, polimorfismo, interfaces e padrões de projeto em Java."
      },
      {
        "id": 9,
        "nome": "Álgebra Linear",
        "descricao": "Vetores, matrizes, sistemas lineares, autovalores e transformações lineares."
      },
      {
        "id": 10,
        "nome": "Software Básico",
        "descricao": "Representação de dados, assembly, organização de memória e sistema operacional."
      },
      {
        "id": 11,
        "nome": "Programação Modular",
        "descricao": "Modularização, TADs, testes automatizados e documentação de software em C."
      },
      {
        "id": 12,
        "nome": "Circuitos Elétricos I",
        "descricao": "Leis de Kirchhoff, circuitos resistivos, capacitores, indutores e análise de circuitos."
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