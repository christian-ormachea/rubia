from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_notas, name='notas'),
    path('nueva/', views.crear_nota, name='nota_crear'),
    path('<int:pk>/editar/', views.editar_nota, name='nota_editar'),
    path('<int:pk>/eliminar/', views.eliminar_nota, name='nota_eliminar'),
]