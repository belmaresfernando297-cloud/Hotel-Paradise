
from django.shortcuts import render
from django.db.models import Sum, Count

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion

from django.contrib.auth.decorators import login_required


@login_required
def inicio(request):

    # Contar los clientes registrados
    total_clientes = Cliente.objects.count()

    # Contar las habitaciones
    total_habitaciones = Habitacion.objects.count()

    # Contar las reservaciones
    total_reservaciones = Reservacion.objects.count()

    # Contar las habitaciones disponibles
    habitaciones_disponibles = Habitacion.objects.filter(
        disponible=True
    ).count()

    # Calcular los ingresos sin incluir reservaciones canceladas
    ingresos = Reservacion.objects.filter(
        estado__in=['Activa', 'Finalizada']
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    # Reporte de reservaciones por estado
    reservaciones_por_estado = Reservacion.objects.values(
        'estado'
    ).annotate(
        cantidad=Count('id')
    ).order_by('estado')

    # Reporte de habitaciones por tipo
    habitaciones_por_tipo = Habitacion.objects.values(
        'tipo'
    ).annotate(
        cantidad=Count('id')
    ).order_by('tipo')

    # Consultar las cinco reservaciones más recientes
    ultimas_reservaciones = Reservacion.objects.select_related(
        'cliente', 'habitacion'
    ).order_by('-id')[:5]

    # Preparar información para el Dashboard
    contexto = {
        'total_clientes': total_clientes,
        'total_habitaciones': total_habitaciones,
        'total_reservaciones': total_reservaciones,
        'habitaciones_disponibles': habitaciones_disponibles,
        'ingresos': ingresos,
        'reservaciones_por_estado': reservaciones_por_estado,
        'habitaciones_por_tipo': habitaciones_por_tipo,
        'ultimas_reservaciones': ultimas_reservaciones,
    }

    return render(request, 'dashboard.html', contexto)
