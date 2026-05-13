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
        related_name='disciplina' 
    )
    titulo = models.CharField(max_length = 200) 

class Conteudo(models.Model):
    topico = models.ForeignKey(
        Topico, 
        on_delete=models.CASCADE, 
        related_name='topico' 
    )
    titulo = models.CharField(max_length = 30)
    descricao = models.TextField()
    conteudo = ''

class Turma(models.Model):
    professor  = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE, 
        related_name='nome do(a) professor(a)' 
    )
    turma = models.CharField(max_length = 3)
    semestre = models.Charfield(max_length = 6)
    horario = models.DateField()

class Materia(m)

class Professor(models.Model):
    nome = models.CharFied(max_length = 100)
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE, 
        related_name='disciplina'         
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE, 
        related_name='turma'  
    )
