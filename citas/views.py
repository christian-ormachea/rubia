from django.shortcuts import render, redirect
import calendar
from datetime import date
from .models import Cita



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
        'nombre_mes': calendar.month_name[mes],
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
        else:
            Cita.objects.create(
                titulo=request.POST['titulo'],
                descripcion=request.POST.get('descripcion', ''),
                fecha=request.POST['fecha'],
                hora=request.POST.get('hora') or None,
                plan=request.POST['plan'],
            )

    anio = request.POST.get('anio', '')
    mes = request.POST.get('mes', '')
    return redirect(f'/calendario/?anio={anio}&mes={mes}')

##Se define la vista para eliminar la cita cuando se clickea una fecha que tiene una cita agendada.
def eliminar_cita(request, cita_id):
    cita = Cita.objects.get_object_or_404(cita_id)
    cita.delete()
    anio = request.POST.get('anio', '')
    mes = request.POST.get('mes', '')

    return redirect(f'/calendario/?anio={anio}&mes={mes}')
