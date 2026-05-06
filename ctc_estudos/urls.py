from django.contrib import admin
from django.urls import path, re_path
import os
from django.conf import settings
from django.conf.urls.static import static
from ctcEstudos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.paginaCadastro, name='cadastro'),
    path('disciplinas/', views.paginaDisciplinas, name='disciplinas'),
    path('flashcards/', views.paginaFlashcards, name='flashcards'),
    path('duvidas/', views.paginaDuvidas, name='duvidas'),
    path('chat/', views.paginaChat, name='chat'),
    path('disciplinas/<str:nome>/', views.paginaDisciplinaDetalhe, name='disciplina_detalhe'),
]

# Servir arquivos estáticos do build do React ANTES da rota catch-all
urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'dist', 'assets'))
urlpatterns += static('/static/', document_root=settings.BASE_DIR)

# Rota catch-all para a landing page (DEVE SER A ÚLTIMA)
urlpatterns += [
    re_path(r'^.*$', views.paginaInicial, name='home'),
]
