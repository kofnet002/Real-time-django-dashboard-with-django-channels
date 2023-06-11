from django.urls import path
from .views import main, dashboard, chat_data

# app_name = 'netvibe'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:room_name>', views.room, name='room'),


    path('', main, name='main'),
    path('<str:slug>/', dashboard, name='dashboard'),
    path('<str:slug>/chart/', chat_data, name='chat_data'),
]
