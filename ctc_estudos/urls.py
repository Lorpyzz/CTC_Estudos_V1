from django.contrib import admin
from django.urls import path

from views import chat


urlpatterns = [

    path('admin/', admin.site.urls),

    path('chat/', chat.chat_view, name='chat'),

]
