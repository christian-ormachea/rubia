from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendario, name='calendario'),
    path('agregar/', views.agregar_cita, name='agregar_cita'),
]