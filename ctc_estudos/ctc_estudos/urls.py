
from django.urls import path
from views import disciplinas, home

urlpatterns = [
    path('', home.home, name='home'),

    path(
        'disciplinas/',
        disciplinas.lista_disciplinas,
        name='lista_disciplinas'
    ),
]