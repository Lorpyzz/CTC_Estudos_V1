from django.urls import path, include
from views import disciplinas, home, flashcards, duvidas, chat, login, forms, cadastro  

urlpatterns = [
    path('', home.home, name='home'),
    path('disciplinas/', disciplinas.lista_disciplinas, name='lista_disciplinas'),
    path('flashcards/', flashcards.flashcards, name='flashcards'),
    path('duvidas/', duvidas.duvidas, name='duvidas'),
    path('login/', login.login, name='login'),
    path('novas/', forms.forms, name='novas'), 
    path('cadastro/', cadastro.cadastro, name='cadastro'),
    path('chat/', include('chat.urls')),
]