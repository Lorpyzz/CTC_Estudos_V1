from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length = 100)
    matricula = models.CharField(max_length = 7)
    email = models.CharField(max_length = 50)
    data_nasc = models.DateField()
    monitor = models.BooleanField()

class Disciplina(models.Model):
    nome = models.CharField(max_length = 30)
    codigo = models.CharField(max_length = 7)
    descricao = models.TextField()
    departamento = models.CharField(max_length = 30)
   
class Topico(models.Model):
    disciplina = models.ForeignKey(
        Disciplina, 
        on_delete=models.CASCADE, 
        related_name='topicos' 
    )
    titulo = models.CharField(max_length = 200) 
