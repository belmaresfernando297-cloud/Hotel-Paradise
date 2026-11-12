from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('registrar/', views.registrar, name='registrar'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
]
