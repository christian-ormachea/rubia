from django.shortcuts import render, redirect, get_object_or_404
import calendar
from datetime import date
from .models import Cita
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

MESES_ES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
}

@login_required
def calendario(request):
    hoy = date.today()
    anio = int(request.GET.get('anio', hoy.year))
    mes = int(request.GET.get('mes', hoy.month))

    mes_anterior = mes - 1
    anio_mes_anterior = anio
    if mes_anterior == 0:
        mes_anterior = 12
        anio_mes_anterior = anio - 1

    mes_siguiente = mes + 1
    anio_mes_siguiente = anio
    if mes_siguiente == 13:
        mes_siguiente = 1
        anio_mes_siguiente = anio + 1


    cal = calendar.Calendar(firstweekday=6)
    dias_del_mes = cal.monthdayscalendar(anio, mes)
    citas_del_mes = Cita.objects.filter(fecha__year=anio, fecha__month=mes).order_by('hora')
    citas_por_dia = {}

    for cita in citas_del_mes:
        citas_por_dia.setdefault(cita.fecha.day, []).append(cita)

    semanas = []
    for semana in dias_del_mes:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append(None)
            else:
                fila.append({
                    'numero': dia,
                    'citas': citas_por_dia.get(dia, [])
                })
        semanas.append(fila)

    contexto = {
        'semanas': semanas,
        'nombre_mes': MESES_ES[mes],
        'anio': anio,
        'mes': mes,
        'dias_semana': ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        'planes': Cita.PLAN_CHOICES,
        'mes_anterior': mes_anterior,
        'anio_mes_anterior': anio_mes_anterior,
        'mes_siguiente': mes_siguiente,
        'anio_mes_siguiente': anio_mes_siguiente,
    }

    return render(request, 'citas/calendario.html', contexto)

##En esta funcion se agrega la funcionalidad (la logica) para agregar un formulario al agendar una cita
##La idea es que se maneje la logica unicamente.
@login_required
def agregar_cita(request):
    if request.method == 'POST':
        cita_id = request.POST.get('cita_id')
        if cita_id:
            cita = Cita.objects.get(id=cita_id)
            cita.titulo = request.POST['titulo']
            cita.descripcion = request.POST.get('descripcion', '')
            cita.fecha = request.POST['fecha']
            cita.hora = request.POST.get('hora') or None
            cita.plan = request.POST['plan']
            cita.save()
            cita.refresh_from_db()
            notificar_cita(cita, request.user, es_nueva=False)
        else:
            cita = Cita.objects.create(
            titulo=request.POST['titulo'],
            descripcion=request.POST.get('descripcion', ''),
            fecha=request.POST['fecha'],
            hora=request.POST.get('hora') or None,
            plan=request.POST['plan'],
            )
            cita.refresh_from_db()
            notificar_cita(cita, request.user, es_nueva=True)

    anio = request.POST.get('anio', '')
    mes = request.POST.get('mes', '')
    return redirect(f'/calendario/?anio={anio}&mes={mes}')

##Se define la vista para eliminar la cita cuando se clickea una fecha que tiene una cita agendada.
@login_required
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.delete()
    anio = request.POST.get('anio', '')
    mes = request.POST.get('mes', '')

    return redirect(f'/calendario/?anio={anio}&mes={mes}')


def notificar_cita(cita, usuario_que_agenda, es_nueva=True):
    if usuario_que_agenda.username == 'chuuky':
        destinatario = settings.EMAIL_PAREJA
    else:
        destinatario = settings.EMAIL_CHRISTIAN

    accion = 'Nueva cita' if es_nueva else 'Cita actualizada'
    asunto = f'{accion}: {cita.titulo} 💙'
    mensaje = (
        f'{usuario_que_agenda.username} {"agendó" if es_nueva else "actualizó"} una cita:\n\n'
        f'Título: {cita.titulo}\n'
        f'Plan: {cita.get_plan_display()}\n'
        f'Fecha: {cita.fecha.strftime("%d/%m/%Y")}\n'
        f'Hora: {cita.hora.strftime("%H:%M") if cita.hora else "Sin definir"}\n'
        f'Descripción: {cita.descripcion or "Sin descripción"}'
    )

    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        [destinatario],
        fail_silently=False,
    )
