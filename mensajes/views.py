from django.shortcuts import render
from .models import Mensaje
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    mensajes = Mensaje.objects.filter(activo=True)
    return render(request, 'mensajes/inicio.html', {'mensajes': mensajes})
