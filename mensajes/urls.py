from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('popup-bienvenida/', views.guardar_preferencia_popup, name='guardar_preferencia_popup'),
    path('cambiar-contrasena/', views.cambiar_contrasena_forzado, name='cambiar_contrasena_forzado'),
    path('chocolate-secreto/', views.activar_chocolate, name='activar_chocolate'),
]