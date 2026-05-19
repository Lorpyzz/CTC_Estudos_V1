from django.urls import path
from views import disciplinas, home, flashcards, duvidas, chat, login

urlpatterns = [
    path('', home.home, name='home'),
    path('disciplinas/', disciplinas.lista_disciplinas, name='lista_disciplinas'),
    path('flashcards/', flashcards.flashcards, name='flashcards'),
    path('duvidas/', duvidas.duvidas, name='duvidas'),
    path('chat/', chat.chat, name='chat'),
    path('login/', login.login, name='login'),

]