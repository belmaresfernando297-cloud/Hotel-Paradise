
from django import forms
from .models import Habitacion


class HabitacionForm(forms.ModelForm):

    class Meta:
        model = Habitacion

        fields = [
            'numero',
            'tipo',
            'precio_noche',
            'capacidad',
            'disponible',
            'imagen',
        ]

        widgets = {
            'numero': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'tipo': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'precio_noche': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
                }
            ),

            'capacidad': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'disponible': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),

            'imagen': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
        }
