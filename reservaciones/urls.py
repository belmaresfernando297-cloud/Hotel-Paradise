
from django.urls import path
from . import views

app_name = 'reservaciones'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('registrar/', views.registrar, name='registrar'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('cancelar/<int:id>/', views.cancelar, name='cancelar'),
]
