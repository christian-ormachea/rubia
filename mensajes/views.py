from django.shortcuts import render
from .models import Mensaje

def inicio(request):
    mensajes = Mensaje.objects.filter(activo=True)
    return render(request, 'mensajes/inicio.html', {'mensajes': mensajes})
