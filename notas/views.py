from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NotaForm
from .models import Nota, NotaImagen


@login_required
def lista_notas(request):
    notas = Nota.objects.all()
    return render(request, 'notas/lista.html', {'notas': notas})


@login_required
def crear_nota(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NotaForm(request.POST, request.FILES)
            if form.is_valid():
                nota = form.save(commit=False)
                nota.autor = request.user
                nota.save()

                for foto in request.FILES.getlist('fotos'):
                    NotaImagen.objects.create(nota=nota, imagen=foto)

                return redirect('notas')
        else:
            form = NotaForm()
    else:
        raise PermissionDenied
    return render(request, 'notas/form.html', {'form': form})


@login_required
def editar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)

    if not request.user.is_superuser:
        raise PermissionDenied

    if nota.autor != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = NotaForm(request.POST, request.FILES, instance=nota)
        if form.is_valid():
            form.save()

            ids_a_eliminar = request.POST.getlist('eliminar_imagen')
            if ids_a_eliminar:
                NotaImagen.objects.filter(id__in=ids_a_eliminar, nota=nota).delete()

            for foto in request.FILES.getlist('fotos'):
                NotaImagen.objects.create(nota=nota, imagen=foto)

            return redirect('notas')
    else:
        form = NotaForm(instance=nota)
    return render(request, 'notas/form.html', {'form': form, 'editar': True, 'nota': nota})


@login_required
def eliminar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)

    if not request.user.is_superuser:
        raise PermissionDenied

    if nota.autor != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        nota.delete()
        return redirect('notas')
    return render(request, 'notas/eliminar_confirmar.html', {'nota': nota})