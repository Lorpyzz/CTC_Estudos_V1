from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'email', 'data_nasc', 'monitor']
        widgets = {
            'data_nasc': forms.DateInput(attrs={'type': 'date'}),
        }
