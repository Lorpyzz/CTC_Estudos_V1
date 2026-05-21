from django import forms
from .models import User, Professor, Disciplina, Turma, InscricaoTurma, Topico, Conteudo, Monitoria, SessaoEstudo

class AlunoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nome', 'matricula', 'email', 'data_nasc']
        widgets = {
            'data_nasc': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome completo', 'style': 'text-transform: uppercase;'}),
            'matricula': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Matrícula'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'E-mail'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        concluida = cleaned_data.get('concluida')
        nota_final = cleaned_data.get('nota_final')
        if concluida and (nota_final is None or nota_final < 5.0):
            raise forms.ValidationError("Para marcar como concluída, a nota final deve ser informada e maior ou igual a 5.0.")
        return cleaned_data

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'email', 'departamento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do Professor', 'style': 'text-transform: uppercase;'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'E-mail', 'style': 'text-transform: uppercase;'}),
            'departamento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Departamento'}),
        }

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'codigo', 'descricao', 'departamento', 'email']
        labels = {
            'nome': 'nome da disciplina',
            'descricao': 'descricao',
            'email': 'email do professor',
            'departamento': 'departamento',
            'codigo': 'código'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'nome da disciplina', 'style': 'text-transform: uppercase;'}),
            'codigo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'código', 'style': 'text-transform: uppercase;'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'descricao', 'rows': 4}),
            'departamento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'departamento', 'style': 'text-transform: uppercase;'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email do professor'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper()
            query = Disciplina.objects.filter(codigo__iexact=codigo)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError('Já existe uma disciplina cadastrada com este código.')
        return codigo

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome:
            nome = nome.upper()
            query = Disciplina.objects.filter(nome__iexact=nome)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError('Já existe uma disciplina cadastrada com este nome.')
        return nome

    def clean_departamento(self):
        departamento = self.cleaned_data.get('departamento')
        if departamento:
            departamento = departamento.upper()
        return departamento

class TurmaForm(forms.ModelForm):
    disciplina = forms.CharField(
        label='Disciplina',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Código (Ex: INF1007)',
            'style': 'text-transform: uppercase;',
            'pattern': '.*[0-9].*',
            'title': 'Deve conter números'
        })
    )
    professor = forms.CharField(
        label='Professor',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nome do Professor',
            'style': 'text-transform: uppercase;'
        })
    )

    class Meta:
        model = Turma
        fields = ['disciplina', 'professor', 'codigo_turma', 'semestre', 'horario']
        widgets = {
            'codigo_turma': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 33A', 'style': 'text-transform: uppercase;'}),
            'semestre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 2026.1'}),
            'horario': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 3ª e 5ª às 11:00'}),
        }

    def clean_disciplina(self):
        val = self.cleaned_data.get('disciplina', '').upper()
        if not any(char.isdigit() for char in val):
            raise forms.ValidationError("A disciplina deve conter números (Ex: INF1007).")

        disciplina = Disciplina.objects.filter(codigo__iexact=val).first()
        if not disciplina:
            disciplina = Disciplina.objects.filter(nome__iexact=val).first()
            if not disciplina:
                disciplina = Disciplina.objects.create(codigo=val, nome=val, departamento="Indefinido")

        return disciplina

    def clean_professor(self):
        val = self.cleaned_data.get('professor', '').upper()
        professor = Professor.objects.filter(nome__iexact=val).first()
        if not professor:
            # Cria o professor automaticamente se não existir
            email = val.replace(" ", "").lower() + "@inf.puc-rio.br"
            professor = Professor.objects.create(nome=val, email=email, departamento="Indefinido")
        return professor

class InscricaoTurmaForm(forms.ModelForm):
    class Meta:
        model = InscricaoTurma
        fields = ['user', 'turma', 'concluida', 'nota_final']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'turma': forms.Select(attrs={'class': 'form-select', 'style': 'text-transform: uppercase;'}),
            'nota_final': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Nota Final'}),
        }

class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ['disciplina', 'titulo_topico']
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'titulo_topico': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Título do Tópico', 'style': 'text-transform: uppercase;'}),
        }

class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ['topico', 'titulo', 'descricao', 'link_material']
        widgets = {
            'topico': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Título do Conteúdo', 'style': 'text-transform: uppercase;'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Descrição...', 'rows': 4}),
            'link_material': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'URL do Material'}),
        }

class MonitoriaForm(forms.ModelForm):
    class Meta:
        model = Monitoria
        fields = ['monitor', 'disciplina', 'semestre_atuacao']
        widgets = {
            'monitor': forms.Select(attrs={'class': 'form-select'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'semestre_atuacao': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 2026.1'}),
        }

class SessaoEstudoForm(forms.ModelForm):
    class Meta:
        model = SessaoEstudo
        fields = ['aluno', 'topico', 'duracao_minutos', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'topico': forms.Select(attrs={'class': 'form-select'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Duração (minutos)'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Observações...', 'rows': 4}),
        }
