
from django.urls import path
from . import views

app_name = 'habitaciones'

urlpatterns = [
    # Mostrar habitaciones
    path('', views.lista_habitaciones, name='lista'),

    # Registrar habitación
    path('crear/', views.crear_habitacion, name='crear'),

    # Editar habitación
    path(
        'editar/<int:id>/',
        views.editar_habitacion,
        name='editar'
    ),

    # Eliminar habitación
    path(
        'eliminar/<int:id>/',
        views.eliminar_habitacion,
        name='eliminar'
    ),
]
