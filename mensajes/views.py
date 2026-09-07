from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from citas.models import Cita
from notas.models import Nota
from .models import Mensaje

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

    contexto = {
        'mensajes': mensajes,
        'semana_actual': semana_actual,
        'ultima_nota': ultima_nota,
    }
    return render(request, 'mensajes/inicio.html', contexto)