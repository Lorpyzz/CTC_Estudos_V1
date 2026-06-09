from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class CtcEstudosUser(AbstractUser):

    nome = models.CharField(max_length=100)

    is_monitor = models.BooleanField(default= False)

    matricula = models.CharField(
        max_length=15,
        unique=True
    )

    data_nasc = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.matricula} - {self.nome or self.username}"


class Professor(models.Model):

    nome = models.CharField(max_length=100)

    email = models.EmailField(
        max_length=100,
        unique=True
    )

    departamento = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome


class Disciplina(models.Model):

    nome = models.CharField(max_length=100)

    codigo = models.CharField(
        max_length=10,
        unique=True
    )

    descricao = models.TextField(
        blank=True,
        null=True
    )

    departamento = models.CharField(max_length=50)

    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    def save(self, *args, **kwargs):
        for campo in self._meta.fields:
            if isinstance(campo, (models.CharField, models.TextField)):
                valor = getattr(self, campo.name)

                if isinstance(valor, str):
                    setattr(self, campo.name, valor.upper())
                    
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(
            "Não é permitido excluir disciplinas."
        )


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

    codigo_turma = models.CharField(max_length=3)

    semestre = models.CharField(max_length=6)

    horario = models.CharField(max_length=100)

    alunos = models.ManyToManyField(
        CtcEstudosUser,
        through='InscricaoTurma',
        related_name='turmas_inscritas'
    )

    def __str__(self):
        return f"{self.disciplina.codigo} ({self.codigo_turma}) - {self.semestre}"


class InscricaoTurma(models.Model):

    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('CANCELADA', 'Cancelada'),
        ('CONCLUIDA', 'Concluída'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ATIVA'
    )
    
    user = models.ForeignKey(
        CtcEstudosUser,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )

    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )

    nota_final = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('user', 'turma')

    verbose_name = "Inscrição em Turma"

    verbose_name_plural = "Inscrições em Turmas"

    def __str__(self):

        status = (
            "Concluída"
            if self.concluida
            else "Em Andamento"
        )

        return f"{self.user.username} em {self.turma} ({status})"


class Topico(models.Model):

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        related_name='topicos'
    )

    titulo_topico = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Tópico"

    def __str__(self):

        return (
            f"{self.disciplina.codigo}"
            f" -> {self.titulo_topico}"
        )


class Conteudo(models.Model):

    topico = models.ForeignKey(
        Topico,
        on_delete=models.CASCADE,
        related_name='conteudos'
    )

    titulo = models.CharField(max_length=100)

    descricao = models.TextField()

    link_material = models.URLField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Conteúdo"

    def __str__(self):
        return self.titulo


class Monitoria(models.Model):

    monitor = models.ForeignKey(
        CtcEstudosUser,
        on_delete=models.CASCADE,
        related_name='monitorias'
    )

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        related_name='monitorias_ativas'
    )

    semestre_atuacao = models.CharField(max_length=6)

    sala = models.CharField(
        max_length=50,
        blank=True
    )

    dia_semana = models.CharField(
        max_length=20, 
        default='sábado'
    )

    horario = models.CharField(
        max_length=50, 
        default='19h - 21h'
    )

    online = models.BooleanField(
        default=False
    )

    link_reuniao = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):

        nome_aluno = (
            self.monitor.first_name
            if self.monitor.first_name
            else self.monitor.username
        )

        return (
            f"Monitor {nome_aluno}"
            f" - {self.disciplina.nome}"
            f" ({self.semestre_atuacao})"
        )

    def clean(self):

        super().clean()
          
        user = self.monitor

        ja_cursou = InscricaoTurma.objects.filter(
            user=self.monitor,
            turma__disciplina=self.disciplina,
            status='CONCLUIDA'
        ).exists()

        if not ja_cursou:
            raise ValidationError(
                f"O aluno '{self.monitor.nome}' não concluiu "
                f"'{self.disciplina.nome}'."
            )

        if self.online and not self.link_reuniao:
            raise ValidationError(
                "Monitorias online devem possuir um link de reunião."
            )

        if not self.online and not self.sala:
            raise ValidationError(
                "Monitorias presenciais devem possuir uma sala."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)


class SessaoEstudo(models.Model):
    aluno = models.ForeignKey(
        CtcEstudosUser,
        on_delete=models.CASCADE,
        related_name='sessoes_estudo'
    )
    disciplina = models.ForeignKey(
        Disciplina,
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
        nome_aluno = (
            self.aluno.first_name
            if self.aluno.first_name
            else self.aluno.username
        )
        
        disciplina_nome = (
            self.disciplina.nome  
            if self.disciplina
            else "Disciplina Removida"
        )

        return (
            f"{nome_aluno} dedicou "
            f"{self.duracao_minutos}min "
            f"em {disciplina_nome}"
        )


# CHAT

class Chat(models.Model):

    usuario1 = models.ForeignKey(
        CtcEstudosUser,
        on_delete=models.CASCADE,
        related_name='chats_usuario1'
    )

    usuario2 = models.ForeignKey(
        CtcEstudosUser,
        on_delete=models.CASCADE,
        related_name='chats_usuario2'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.usuario1} x {self.usuario2}"


class Mensagem(models.Model):

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='mensagens'
    )

    usuario = models.ForeignKey(
        CtcEstudosUser,
        on_delete=models.CASCADE
    )

    conteudo = models.TextField()

    enviado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['enviado_em']

    def __str__(self):

        return (
            f"{self.usuario.username}: "
            f"{self.conteudo[:20]}"
        )