from django.shortcuts import render, redirect

# "banco" mockado — fica em memória enquanto o servidor estiver rodando
disciplinas = [
    {"id": 1, "nome": "Programação",                   "codigo": "INF1000"},
    {"id": 2, "nome": "Estruturas de Dados",           "codigo": "INF1010"},
    {"id": 3, "nome": "Estruturas de Dados Avançadas", "codigo": "INF1100"},
    {"id": 4, "nome": "Cálculo I",                     "codigo": "MAT1000"},
    {"id": 5, "nome": "Cálculo II",                    "codigo": "MAT1110"},
]

decks = []

def flashcards(request):
    if request.method == 'POST':
        nome_deck     = request.POST.get('nome_deck', '').strip()
        disciplina_id = request.POST.get('disciplina_id', '').strip()

        # busca a disciplina pelo id
        disciplina = None
        for d in disciplinas:
          if str(d['id']) == disciplina_id:
            disciplina = d
            break

        if not nome_deck or not disciplina:
            return render(request, 'flashcards.html', {
                'disciplinas': disciplinas,
                'decks': decks,
                'erro': 'Preencha todos os campos.',
            })

        # salva o deck no "banco"
        decks.append({
            'nome':              nome_deck,
            'disciplina_nome':   disciplina['nome'],
            'disciplina_codigo': disciplina['codigo'],
        })

        return redirect('flashcards')

    return render(request, 'flashcards.html', {
        'disciplinas': disciplinas,
        'decks': decks,
    })