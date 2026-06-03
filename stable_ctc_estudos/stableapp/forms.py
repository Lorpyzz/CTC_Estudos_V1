from django import forms
from django.contrib.auth.hashers import make_password
from .models import CtcEstudosUser, Professor, Disciplina, Turma, InscricaoTurma, Topico, Conteudo, Monitoria, SessaoEstudo


class AlunoForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Crie uma senha'})
    )

    class Meta:
        model = CtcEstudosUser
        fields = ['nome', 'matricula', 'email', 'data_nasc'] 
        labels = {
            'nome': 'Nome completo',
            'matricula': 'Matrícula',
            'email': 'E-mail',
            'data_nasc': 'Data de nascimento',
            
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome completo', 'style': 'text-transform: uppercase;'}),
            'matricula': forms.TextInput(attrs={'class':'form-input', 'placeholder': '1920567'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'E-mail'}),
            'data_nasc': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'email', 'departamento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do Professor', 'style': 'text-transform: uppercase;'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'E-mail'}),
            'departamento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Departamento', 'style': 'text-transform: uppercase;'}),
        }

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'codigo', 'descricao', 'departamento', 'email']
        labels = {
            'nome': 'Nome da disciplina',
            'descricao': 'Descricao',
            'email': 'Email do professor',
            'departamento': 'Departamento',
            'codigo': 'Código'
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
            query = Disciplina.objects.filter(codigo__iexact=codigo)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError('Já existe uma disciplina cadastrada com este código.')
        return codigo

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome:
            query = Disciplina.objects.filter(nome__iexact=nome)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError('Já existe uma disciplina cadastrada com este nome.')
        return nome

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['disciplina'].initial = self.instance.disciplina.codigo
            self.fields['professor'].initial = self.instance.professor.nome
            if user:
                if not user.is_monitor:
                    self.fields['professor'].disabled = True

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
        if self.fields['professor'].disabled:
            return self.instance.professor
        val = self.cleaned_data.get('professor', '').upper()
        professor = Professor.objects.filter(nome__iexact=val).first()
        if not professor:
            email = val.replace(" ", "").lower() + "@inf.puc-rio.br"
            professor = Professor.objects.create(nome=val, email=email, departamento="Indefinido")
        return professor

class InscricaoTurmaForm(forms.ModelForm):
    class Meta:
        model = InscricaoTurma
        fields = ['turma', 'status', 'nota_final']

        widgets = {
            'turma': forms.Select(attrs={'class': 'form-select', 'style': 'text-transform: uppercase;'}),
            'status': forms.Select(attrs={'class': 'form-select'}), 
            'nota_final': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Nota Final'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        nota_final = cleaned_data.get('nota_final')

        if status == 'CONCLUIDA':
            if nota_final is None or nota_final < 5.0:
                raise forms.ValidationError(
                    "Para marcar como concluída, a nota final deve ser informada e maior ou igual a 5.0."
                )
        
        else:
            if nota_final is not None:
                raise forms.ValidationError(
                    "Você não pode inserir uma nota final para uma inscrição que não está concluída."
                )
        return cleaned_data

class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ['disciplina', 'titulo_topico']
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'titulo_topico': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Título do Tópico',
                                                     'style': 'text-transform: uppercase;'}),
        }

class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ['topico', 'titulo', 'descricao', 'link_material']
        widgets = {
            'topico': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Título do Conteúdo',
                                              'style': 'text-transform: uppercase;'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 
                                               'placeholder': 'Descrição...', 'rows': 4}),
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
        fields = ['topico', 'duracao_minutos', 'observacoes']
        widgets = {
            'topico': forms.Select(attrs={'class': 'form-select'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Duração (minutos)'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Observações...', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            turmas_do_aluno = InscricaoTurma.objects.filter(user=user, status__in=['ATIVA', 'CONCLUIDA']).values_list('turma', flat=True)
            disciplinas_do_aluno = Turma.objects.filter(id__in=turmas_do_aluno).values_list('disciplina', flat=True)
            self.fields['topico'].queryset = Topico.objects.filter(disciplina__in=disciplinas_do_aluno)