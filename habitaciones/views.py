
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Habitacion
from .forms import HabitacionForm
from reservaciones.models import Reservacion

from django.contrib.auth.decorators import login_required


# Mostrar todas las habitaciones
@login_required
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all().order_by('numero')

    contexto = {
        'habitaciones': habitaciones,
    }

    return render(
        request,
        'habitaciones/lista.html',
        contexto
    )


# Registrar una habitación
@login_required
def crear_habitacion(request):
    if request.method == 'POST':
        formulario = HabitacionForm(
            request.POST,
            request.FILES
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Habitación registrada correctamente.')
            return redirect('habitaciones:lista')
    else:
        formulario = HabitacionForm()

    contexto = {
        'formulario': formulario,
    }

    return render(
        request,
        'habitaciones/formulario.html',
        contexto
    )


# Editar una habitación
@login_required
def editar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)

    if request.method == 'POST':
        formulario = HabitacionForm(
            request.POST,
            request.FILES,
            instance=habitacion
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Habitación actualizada correctamente.')
            return redirect('habitaciones:lista')
    else:
        formulario = HabitacionForm(instance=habitacion)

    contexto = {
        'formulario': formulario,
        'editar': True,
        'habitacion': habitacion,
    }

    return render(
        request,
        'habitaciones/formulario.html',
        contexto
    )


# Eliminar una habitación
@login_required
def eliminar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)

    if request.method == 'POST':
        tiene_reservaciones_activas = Reservacion.objects.filter(
            habitacion=habitacion,
            estado='Activa'
        ).exists()

        if tiene_reservaciones_activas:
            messages.error(
                request,
                'No se puede eliminar esta habitación porque tiene reservaciones activas.'
            )
        else:
            habitacion.delete()
            messages.success(request, 'Habitación eliminada correctamente.')

    return redirect('habitaciones:lista')
