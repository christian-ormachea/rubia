from django.shortcuts import render
import random
from .models import Mensaje

def inicio(request):
    mensajes_activos = Mensaje.objects.filter(activo=True)
    mensaje = random.choice(mensajes_activos) if mensajes_activos else None
    return render(request, 'mensajes/inicio.html', {'mensaje': mensaje})

