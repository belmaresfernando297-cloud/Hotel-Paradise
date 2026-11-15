
from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente

        fields = [
            'nombre',
            'apellidos',
            'correo',
            'telefono',
        ]

        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'apellidos': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'correo': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),

            'telefono': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }

        error_messages = {
            'correo': {
                'unique': 'Ya existe un cliente registrado con este correo electrónico.',
            }
        }
