from datetime import timedelta

from django.shortcuts import redirect
from django.utils import timezone

from .models import PreferenciaUsuario

DIAS_LIMITE_CONTRASENA = 30
RUTAS_EXENTAS = ['/cambiar-contrasena/', '/logout/', '/static/', '/media/']


class ForzarCambioContrasenaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        usuario = request.user

        if usuario.is_authenticated and not usuario.is_superuser:
            if not any(request.path.startswith(ruta) for ruta in RUTAS_EXENTAS):
                preferencia, _ = PreferenciaUsuario.objects.get_or_create(usuario=usuario)
                tiempo_pasado = timezone.now() - preferencia.contrasena_cambiada_en
                if tiempo_pasado > timedelta(days=DIAS_LIMITE_CONTRASENA):
                    return redirect('cambiar_contrasena_forzado')

        return self.get_response(request)