from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from django.db.models import Q

from django.contrib.auth.decorators import login_required


@login_required
def lista(request):
    busqueda = request.GET.get('buscar', '').strip()

    clientes = Cliente.objects.all()

    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellidos__icontains=busqueda) |
            Q(correo__icontains=busqueda)
        )

    contexto = {
        'clientes': clientes,
        'total_clientes': clientes.count(),
        'busqueda': busqueda,
    }

    return render(request, 'clientes/lista.html', contexto)

@login_required
def registrar(request):
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('clientes:lista')

    else:
        formulario = ClienteForm()

    return render(request, 'clientes/registrar.html', {
        'formulario': formulario
    })

@login_required
def editar(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        formulario = ClienteForm(request.POST, instance=cliente)

        if formulario.is_valid():
            formulario.save()
            return redirect('clientes:lista')

    else:
        formulario = ClienteForm(instance=cliente)

    return render(request, 'clientes/registrar.html', {
        'formulario': formulario,
        'editar': True
    })

@login_required
def eliminar(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()

    return redirect('clientes:lista')
