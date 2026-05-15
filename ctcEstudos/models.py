from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    Extensão do usuário padrão do Django. 
    Centraliza a identidade do Aluno e suas permissões.
    Todo monitor é obrigatoriamente um usuário/aluno do sistema.
    """
    matricula = models.CharField(max_length=15, unique=True)
    is_monitor = models.BooleanField(default=False)
    data_nasc = models.DateField(null=True, blank=True)

    def __str__(self):
        nome = self.first_name if self.first_name else self.username
        return f"{self.matricula} - {nome}"


class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    departamento = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    descricao = models.TextField(blank=True, null=True)
    departamento = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Turma(models.Model):
    disciplina = models.ForeignKey(
        Disciplina, 
        on_delete=models.CASCADE, 
        related_name='turmas'
    )
    professor = models.ForeignKey(
        Professor, 
        on_delete=models.PROTECT, 
        related_name='turmas_ministradas'
    )
    codigo_turma = models.CharField(max_length=3) # Ex: "33A"
    semestre = models.CharField(max_length=6) # Ex: 2026.1
    horario = models.CharField(max_length=100) # Ex: "3ª e 5ª às 11:00"

    alunos = models.ManyToManyField(
        User, 
        through='InscricaoTurma', 
        related_name='turmas_inscritas'
    )

    def __str__(self):
        return f"{self.disciplina.codigo} ({self.codigo_turma}) - {self.semestre}"

class InscricaoTurma(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscricoes')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='inscricoes')
    concluida = models.BooleanField(default=False) # GATILHO DA REGRA DE NEGÓCIO DA MONITORIA
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'turma')
        verbose_name = "Inscrição em Turma"
        verbose_name_plural = "Inscrições em Turmas"

    def __str__(self):
        status = "Concluída" if self.concluida else "Em Andamento"
        return f"{self.user.username} em {self.turma} ({status})"

class Topico(models.Model):

    disciplina = models.ForeignKey(
        Disciplina, 
        on_delete=models.CASCADE, 
        related_name='topicos' 
    )
    titulo = models.CharField(max_length=200) 

    class Meta:
        verbose_name = "Tópico"

    def __str__(self):
        return f"{self.disciplina.codigo} -> {self.titulo}"

class Conteudo(models.Model):
    """ Materiais específicos de estudo vinculados a um Tópico """
    topico = models.ForeignKey(
        Topico, 
        on_delete=models.CASCADE, 
        related_name='conteudos' 
    )
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    link_material = models.URLField(blank=True, null=True) 

    class Meta:
        verbose_name = "Conteúdo"

    def __str__(self):
        return self.titulo

class Monitoria(models.Model):
    
    monitor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'is_monitor': True}, 
        related_name='monitorias'
    )
    disciplina = models.ForeignKey(
        Disciplina, 
        on_delete=models.CASCADE, 
        related_name='monitorias_ativas'
    )
    semestre_atuacao = models.CharField(max_length=6)

    def __str__(self):
        nome_aluno = self.monitor.first_name if self.monitor.first_name else self.monitor.username
        return f"Monitor {nome_aluno} - {self.disciplina.nome} ({self.semestre_atuacao})"

    def clean(self):

        if hasattr(self, 'monitor') and hasattr(self, 'disciplina'):
            ja_cursou = InscricaoTurma.objects.filter(
                user=self.monitor,
                turma__disciplina=self.disciplina,
                concluida=True
            ).exists()

            if not ja_cursou:
                nome_aluno = self.monitor.first_name if self.monitor.first_name else self.monitor.username
                raise ValidationError(
                    f"Inconsistência: O aluno '{nome_aluno}' não possui registro de "
                    f"conclusão na disciplina '{self.disciplina.nome}' e não pode ser alocado como monitor."
                )

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

class SessaoEstudo(models.Model):
    aluno = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sessoes_estudo'
    )
    topico = models.ForeignKey(
        Topico, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='sessoes_direcionadas'
    )
    data_estudo = models.DateField(auto_now_add=True)
    duracao_minutos = models.PositiveIntegerField() 
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Sessão de Estudo"
        verbose_name_plural = "Sessões de Estudo"

    def __str__(self):
        nome_aluno = self.aluno.first_name if self.aluno.first_name else self.aluno.username
        return f"{nome_aluno} dedicou {self.duracao_minutos}min em {self.topico.titulo if self.topico else 'Tópico Geral'}"