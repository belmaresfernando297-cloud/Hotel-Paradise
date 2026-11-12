
from django.db import models
from django.core.exceptions import ValidationError


class Reservacion(models.Model):

    ESTADOS = [
        ('Activa', 'Activa'),
        ('Cancelada', 'Cancelada'),
        ('Finalizada', 'Finalizada'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='reservaciones'
    )

    habitacion = models.ForeignKey(
        'habitaciones.Habitacion',
        on_delete=models.PROTECT,
        related_name='reservaciones'
    )

    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Activa'
    )

    def clean(self):
        super().clean()

        if self.fecha_entrada and self.fecha_salida:
            if self.fecha_salida <= self.fecha_entrada:
                raise ValidationError(
                    'La fecha de salida debe ser posterior a la entrada.'
                )

            if self.habitacion_id and self.estado == 'Activa':
                conflictos = Reservacion.objects.filter(
                    habitacion_id=self.habitacion_id,
                    estado='Activa',
                    fecha_entrada__lt=self.fecha_salida,
                    fecha_salida__gt=self.fecha_entrada
                ).exclude(pk=self.pk)

                if conflictos.exists():
                    raise ValidationError(
                        'La habitación ya está reservada en esas fechas.'
                    )

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente}"

