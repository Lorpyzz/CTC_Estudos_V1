from django.contrib import admin
from django.urls import path
import os
from django.conf import settings
from django.conf.urls.static import static
from stableapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro/', views.paginaCadastro, name='cadastro'),
    path('cadastro', views.paginaCadastro),
    path('login/', views.loginAluno, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('config/', views.config, name='config'),

    path('disciplinas/', views.paginaDisciplinas, name='disciplinas'),
    path('disciplinas/novo/', views.form_disciplina, name='form_disciplina'),
    path('disciplinas/update/<int:id>/', views.update_disciplina, name='update_disciplina'),
    path('disciplinas/<str:nome>/', views.paginaDisciplinaDetalhe, name='disciplina_detalhe'),
    
    path('turmas/', views.paginaTurmas, name='turmas'),
    path('turmas/nova/', views.form_turma, name='form_turma'),
    path('turmas/update/<int:id>/', views.update_turma, name='update_turma'),
    path('turmas/delete/<int:id>/', views.delete_turma, name='delete_turma'),
    
    path('sessoes/nova/', views.form_sessao_estudo, name='form_sessao_estudo'),
    path('sessoes/update/<int:id>/', views.update_sessao_estudo, name='update_sessao_estudo'),
    path('sessoes/delete/<int:id>/', views.delete_sessao_estudo, name='delete_sessao_estudo'),
    
    path('inscricoes/nova/', views.form_inscricao, name='form_inscricao'),
    path('inscricoes/update/<int:id>/', views.update_inscricao, name='update_inscricao'),
    path('inscricoes/<int:turma_id>/cancelar/', views.delete_inscricao, name='cancelar_inscricao'),
    
    path('topicos/novo/', views.form_topico, name='form_topico'),
    path('topicos/update/<int:id>/', views.update_topico, name='update_topico'),
    path('topicos/delete/<int:id>/', views.delete_topico, name='delete_topico'),
    
    path('conteudos/novo/', views.form_conteudo, name='form_conteudo'),
    path('conteudos/update/<int:id>/', views.update_conteudo, name='update_conteudo'),
    path('conteudos/delete/<int:id>/', views.delete_conteudo, name='delete_conteudo'),
    
    path('monitorias/nova/', views.form_monitoria, name='form_monitoria'),
    path('monitorias/update/<int:id>/', views.update_monitoria, name='update_monitoria'),
    path('monitorias/delete/<int:id>/', views.delete_monitoria, name='delete_monitoria'),
    
    path('professores/novo/', views.form_professor, name='form_professor'),
    path('professores/update/<int:id>/', views.update_professor, name='update_professor'),
    path('professores/delete/<int:id>/', views.delete_professor, name='delete_professor'),
    
    path('alunos/update/<int:id>/', views.update_aluno, name='update_aluno'),
    path('alunos/delete/<int:id>/', views.delete_aluno, name='delete_aluno'),
    
    path('flashcards/', views.paginaFlashcards, name='flashcards'),
    path('duvidas/', views.paginaDuvidas, name='duvidas'),
    path('chat/', views.paginaChat, name='chat'),
    path('admin/', admin.site.urls),
    path('', views.paginaInicial, name='home'),
    path('monitoria/', views.exibe_monitoria, name='monitoria'),
    path('monitoria/nova/', views.form_monitoria, name='form_monitoria'),
    path('perfil/', views.perfil, name = 'perfil'),
    path('ajuda/', views.ajuda, name = 'ajuda')

]

urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'dist', 'assets'))
urlpatterns += static('/static/', document_root=settings.BASE_DIR)