from django import forms
from django.contrib.auth.hashers import make_password
from .models import CtcEstudosUser, Professor, Disciplina, Turma, InscricaoTurma, Topico, Conteudo, Monitoria, SessaoEstudo, Deck, Flashcard



class AlunoForm(forms.ModelForm):
    
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Crie uma senha'}))

    class Meta:
        model = CtcEstudosUser
        fields = ['nome', 'matricula', 'email', 'data_nasc','is_monitor'] 
        labels = {
            'nome': 'Nome completo',
            'matricula': 'Matrícula',
            'email': 'E-mail',
            'data_nasc': 'Data de nascimento',
            'is_monitor': 'Sou monitor'
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
        return codigo.upper()

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome:
            query = Disciplina.objects.filter(nome__iexact=nome)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError('Já existe uma disciplina cadastrada com este nome.')
        return nome.upper()

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
    
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        label="Disciplina",
        empty_label="---------",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_disciplina'})
    )
    
    turma = forms.CharField(
        label="Código da Turma",
        widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'id': 'id_codigo_turma', 
            'placeholder': 'Escolha ou digite (Ex: 33A)',
            'autocomplete': 'off', 
            'style': 'text-transform: uppercase;'
        })
    )

    class Meta:
        model = InscricaoTurma
        fields = ['disciplina', 'turma', 'status', 'nota_final']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select', 'id': 'id_status'}), 
            'nota_final': forms.NumberInput(attrs={'class': 'form-input', 'id': 'id_nota_final', 'placeholder': 'Nota Final'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.turma:
            self.fields['disciplina'].initial = self.instance.turma.disciplina.id
            
            self.fields['turma'].initial = self.instance.turma.codigo_turma

    def clean_turma(self):
        codigo_digitado = self.cleaned_data.get('turma', '').strip().upper()
        disciplina = self.cleaned_data.get('disciplina')

        if not codigo_digitado:
            raise forms.ValidationError("Este campo é obrigatório.")

        if not disciplina:
            raise forms.ValidationError("Selecione uma disciplina primeiro.")

        
        turma_obj = Turma.objects.filter(codigo_turma=codigo_digitado, disciplina=disciplina).first()
        
        if not turma_obj:
            
            professor_padrao, _ = Professor.objects.get_or_create(
                nome="A DEFINIR",
                defaults={
                    'email': 'adefinir@inf.puc-rio.br',
                    'departamento': 'Indefinido'
                }
            )

            
            turma_obj = Turma.objects.create(
                codigo_turma=codigo_digitado,
                disciplina=disciplina,
                professor=professor_padrao, 
                semestre="2026.1", 
                horario="A definir"
            )
        
        return turma_obj

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
       
        fields = ['topico', 'titulo', 'descricao', 'link_material', 'arquivo']
        
        widgets = {
            'topico': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Semana 1 - Introdução ou Revisão P1'}),
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Título do Conteúdo'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Descrição...', 'rows': 4}),
            'link_material': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'URL do Material (Opcional)'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-input'}),
        }

class MonitoriaForm(forms.ModelForm):

    class Meta:
        model = Monitoria

        fields = [
            'monitor',
            'disciplina',
            'semestre_atuacao',
            'dia_semana',
            'horario',
            'online',
            'sala',
            'link_reuniao'
        ]

        widgets = {
            'monitor': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'disciplina': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'semestre_atuacao': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Ex: 2026.1'
                }
            ),

            'dia_semana': forms.Select(
                choices=[
                    ('Segunda-feira', 'Segunda-feira'),
                    ('Terça-feira', 'Terça-feira'),
                    ('Quarta-feira', 'Quarta-feira'),
                    ('Quinta-feira', 'Quinta-feira'),
                    ('Sexta-feira', 'Sexta-feira'),
                    ('Sábado', 'Sábado')
                ],
                attrs={'class': 'form-select'}
            ),

            'horario': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Ex: 14h - 16h'
                }
            ),

            'sala': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Ex: L456'
                }
            ),

            'link_reuniao': forms.URLInput(
                attrs={
                    'class': 'form-input',
                    'placeholder':
                    'https://meet.google.com/abc-defg-hij'
                }
            ),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                if field_name != 'online':  
                    field.widget.attrs.update({'class': 'form-input'})
        
        def clean(self):
            cleaned_data = super().clean()
            turma = cleaned_data.get("turma")

            if turma:
                aprovado = InscricaoTurma.objects.filter(
                    user=self.user,
                    turma=turma,
                    nota_final__gt=6.0
                ).exists()

                if not aprovado:
                    raise forms.ValidationError(
                        "Você precisa ter concluído essa disciplina com nota superior a 6,0."
                    )
            return cleaned_data


class SessaoEstudoForm(forms.ModelForm):
    METODO_CHOICES = [
        ('', 'Selecione uma opção...'),
        ('direto', 'Conteúdos Diretos'),
        ('teoria', 'Revisar Teoria'),
    ]
    
    metodo_revisao = forms.ChoiceField(
        choices=METODO_CHOICES,
        required=True,
        label="Método de Revisão",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_metodo_revisao'})
    )

    class Meta:
        model = SessaoEstudo
        fields = ['disciplina', 'metodo_revisao', 'duracao_minutos', 'observacoes']

        
        labels = {
            'disciplina': 'Tópico / Disciplina',
            'duracao_minutos': 'Duração (minutos)',
            'observacoes': 'Observações',
        }
        
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Duração (minutos)'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Observações...', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            turmas_do_aluno = InscricaoTurma.objects.filter(
                user=user, 
                status__in=['ATIVA', 'CONCLUIDA']
            ).values_list('turma_id', flat=True).distinct()
            
            disciplinas_do_aluno = Turma.objects.filter(
                id__in=turmas_do_aluno
            ).values_list('disciplina_id', flat=True).distinct()
            
            self.fields['disciplina'].queryset = Disciplina.objects.filter(
                id__in=disciplinas_do_aluno
            )

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['disciplina', 'nome']


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['pergunta', 'resposta']