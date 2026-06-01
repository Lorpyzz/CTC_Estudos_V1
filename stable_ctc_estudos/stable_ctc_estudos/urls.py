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
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('disciplinas/', views.paginaDisciplinas, name='disciplinas'),
    path('disciplinas/novo/', views.form_disciplina, name='form_disciplina'),
    path('disciplinas/update/<id>',views.update_disciplina),
    path('disciplinas/delete/<id>',views.delete_disciplina),
    path('disciplinas/<str:nome>/', views.paginaDisciplinaDetalhe, name='disciplina_detalhe'),
    path('turmas/', views.paginaTurmas, name='turmas'),
    path('turmas/nova/', views.form_turma, name='form_turma'),
    path('sessoes/nova/', views.form_sessao_estudo, name='form_sessao_estudo'),
    path('inscricoes/nova/', views.form_inscricao, name='form_inscricao'),
    path('topicos/novo/', views.form_topico, name='form_topico'),
    path('flashcards/', views.paginaFlashcards, name='flashcards'),
    path('duvidas/', views.paginaDuvidas, name='duvidas'),
    path('chat/', views.paginaChat, name='chat'),
    path('admin/', admin.site.urls),
    path('', views.paginaInicial, name='home'),
]

urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'dist', 'assets'))
urlpatterns += static('/static/', document_root=settings.BASE_DIR)