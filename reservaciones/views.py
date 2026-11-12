
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservacion
from .forms import ReservacionForm
from django.db.models import Q

from django.contrib.auth.decorators import login_required


# Mostrar todas las reservaciones
@login_required
def lista(request):
    busqueda = request.GET.get('buscar', '').strip()

    reservaciones = Reservacion.objects.select_related(
        'cliente', 'habitacion'
    ).all().order_by('-id')

    if busqueda:
        filtros = (
            Q(cliente__nombre__icontains=busqueda) |
            Q(cliente__apellidos__icontains=busqueda) |
            Q(habitacion__tipo__icontains=busqueda)
        )

        if busqueda.isdigit():
            filtros |= Q(habitacion__numero=int(busqueda))

        reservaciones = reservaciones.filter(filtros)

    contexto = {
        'reservaciones': reservaciones,
        'total_reservaciones': reservaciones.count(),
        'busqueda': busqueda,
    }

    return render(request, 'reservaciones/lista.html', contexto)

# Registrar una reservación
@login_required
def registrar(request):

    if request.method == 'POST':
        formulario = ReservacionForm(request.POST)

        if formulario.is_valid():

            reservacion = formulario.save(commit=False)

            # Calcular las noches de hospedaje
            noches = (
                reservacion.fecha_salida -
                reservacion.fecha_entrada
            ).days

            # Calcular el importe total
            reservacion.total = (
                reservacion.habitacion.precio_noche * noches
            )

            reservacion.save()

            return redirect('reservaciones:lista')

    else:
        formulario = ReservacionForm()

    return render(
        request,
        'reservaciones/registrar.html',
        {'formulario': formulario}
    )


# Editar una reservación
@login_required
def editar(request, id):

    reservacion = get_object_or_404(Reservacion, id=id)

    if request.method == 'POST':
        formulario = ReservacionForm(
            request.POST,
            instance=reservacion
        )

        if formulario.is_valid():

            reservacion = formulario.save(commit=False)

            noches = (
                reservacion.fecha_salida -
                reservacion.fecha_entrada
            ).days

            reservacion.total = (
                reservacion.habitacion.precio_noche * noches
            )

            reservacion.save()

            return redirect('reservaciones:lista')

    else:
        formulario = ReservacionForm(instance=reservacion)

    return render(
        request,
        'reservaciones/registrar.html',
        {
            'formulario': formulario,
            'editar': True
        }
    )


# Cancelar una reservación
@login_required
def cancelar(request, id):

    reservacion = get_object_or_404(Reservacion, id=id)

    if request.method == 'POST':
        reservacion.estado = 'Cancelada'
        reservacion.save(update_fields=['estado'])

    return redirect('reservaciones:lista')
