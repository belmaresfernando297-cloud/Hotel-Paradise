
from django import forms
from .models import Reservacion


class ReservacionForm(forms.ModelForm):

    class Meta:
        model = Reservacion

        fields = [
            'cliente',
            'habitacion',
            'fecha_entrada',
            'fecha_salida',
        ]

        widgets = {
            'cliente': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'habitacion': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'fecha_entrada': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'fecha_salida': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }
