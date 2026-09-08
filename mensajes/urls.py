from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('popup-bienvenida/', views.guardar_preferencia_popup, name='guardar_preferencia_popup'),
]