from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from citas.models import Cita
from notas.models import Nota
from .models import Mensaje, PreferenciaUsuario

from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from .forms import CambiarContrasenaForm

DIAS_SEMANA = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']


@login_required
def inicio(request):
    mensajes = Mensaje.objects.filter(activo=True)

    hoy = date.today()
    inicio_semana = hoy - timedelta(days=(hoy.weekday() + 1) % 7)
    fin_semana = inicio_semana + timedelta(days=6)
    citas_semana = Cita.objects.filter(fecha__gte=inicio_semana, fecha__lte=fin_semana).order_by('fecha', 'hora')

    semana_actual = []
    for i in range(7):
        fecha_dia = inicio_semana + timedelta(days=i)
        semana_actual.append({
            'nombre': DIAS_SEMANA[i],
            'numero': fecha_dia.day,
            'es_hoy': fecha_dia == hoy,
            'citas': [c for c in citas_semana if c.fecha == fecha_dia],
        })

    ultima_nota = Nota.objects.order_by('-creada').first()

    preferencia, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
    contexto = {
        'mensajes': mensajes,
        'semana_actual': semana_actual,
        'ultima_nota': ultima_nota,
        'mostrar_popup_bienvenida': not preferencia.oculto_popup_bienvenida,
    }
    return render(request, 'mensajes/inicio.html', contexto)

@login_required
def guardar_preferencia_popup(request):
    if request.method == 'POST':
        preferencia, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
        if request.POST.get('no_volver_a_mostrar'):
            preferencia.oculto_popup_bienvenida = True
            preferencia.save()
    return redirect('inicio')

@login_required
def cambiar_contrasena_forzado(request):
    preferencia, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = CambiarContrasenaForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            preferencia.contrasena_cambiada_en = timezone.now()
            preferencia.save()
            return redirect('inicio')
    else:
        form = CambiarContrasenaForm(request.user)

    return render(request, 'mensajes/cambiar_contrasena.html', {'form': form})

@login_required
def activar_chocolate(request):
    if not request.user.is_superuser:
        preferencia, _ = PreferenciaUsuario.objects.get_or_create(usuario=request.user)
        if not preferencia.chocolate_visto:
            preferencia.chocolate_visto = True
            preferencia.save()
            request.session['mostrar_chocolate'] = True
    return redirect(request.META.get('HTTP_REFERER', 'inicio'))