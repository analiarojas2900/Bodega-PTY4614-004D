from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Material, Ticket, CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import logout
from .roles import ADMINISTRADOR_SISTEMA, ADMINISTRADOR_OBRA, JEFE_OBRA, CAPATAZ, JEFE_BODEGA
from .models import Role
import pdb

# Función para verificar el rol basado en ID
def has_role_id(user, role_id):
    return user.roles.filter(id=role_id).exists()
# Vista principal
def home_view(request):
    return render(request, 'HomeView/home.html')


# Vista de inventario (solo accesible por Jefe de Bodega, Role ID = 5)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def inventory(request):
    return render(request, 'InventoryView/inventory.html')


# Lista de materiales activos e inactivos (solo accesible por Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def lista_view(request):
    materiales_activos = Material.objects.filter(activo=True)
    materiales_inactivos = Material.objects.filter(activo=False)
    return render(request, 'InventoryView/lista.html', {
        'materiales': materiales_activos,
        'inactivos': materiales_inactivos
    })

@login_required
def some_view(request):
    """
    Vista restringida que muestra detalles del usuario autenticado.
    Solo usuarios autenticados pueden acceder a esta vista.
    """
    usuario = request.user
    roles = usuario.roles.all()  # Obtener los roles del usuario

    # Depuración: Imprimir roles en la consola (opcional)
    print(f"Usuario: {usuario.username}, Roles: {roles}")

    context = {
        'usuario': usuario,
        'roles': roles,
        'mensaje': 'Bienvenido a la vista restringida'
    }
    return render(request, 'usuarios/restricted_view.html', context)

# Restaurar material inactivo (solo accesible por Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def restore_material_view(request, id):
    material = get_object_or_404(Material, id=id)
    if request.method == 'POST':
        material.activo = True
        material.save()
        return redirect('lista_view')
    return render(request, 'InventoryView/restaurar.html', {'material': material})


# Agregar material (solo accesible por Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def add_material_view(request):
    if request.method == 'POST':
        material = Material(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            unidad_medida=request.POST.get('unidad_medida'),
            cantidad_disponible=request.POST.get('cantidad_disponible'),
            stock_minimo=request.POST.get('stock_minimo')
        )
        material.save()
        return redirect('lista_view')
    return render(request, 'InventoryView/agregar.html')


# Actualizar material (solo accesible por Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def update_material_view(request, id):
    material = get_object_or_404(Material, id=id)
    if request.method == 'POST':
        material.nombre = request.POST.get('nombre')
        material.descripcion = request.POST.get('descripcion')
        material.unidad_medida = request.POST.get('unidad_medida')
        material.cantidad_disponible = request.POST.get('cantidad_disponible')
        material.stock_minimo = request.POST.get('stock_minimo')
        material.save()
        return redirect('lista_view')
    return render(request, 'InventoryView/editar.html', {'material': material})


# Eliminar material (solo accesible por Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def delete_material_view(request, id):
    material = get_object_or_404(Material, id=id)
    if request.method == 'POST':
        material.activo = False
        material.save()
        return redirect('lista_view')
    return render(request, 'InventoryView/eliminar.html', {'material': material})


# Crear ticket (solo accesible por Jefe de Obra o Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_OBRA) or has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def crear_ticket(request):
    if request.method == 'POST':
        Ticket.objects.create(
            usuario=request.POST.get('usuario'),
            material_solicitado=request.POST.get('material_solicitado'),
            cantidad=request.POST.get('cantidad')
        )
        return redirect('lista_tickets')
    return render(request, 'tickets/crear.html')


# Lista de tickets (solo accesible por Jefe de Obra o Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_OBRA) or has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def lista_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/lista.html', {'tickets': tickets})


# Ver ticket (solo accesible por Jefe de Obra o Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_OBRA) or has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def ver_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'tickets/ver.html', {'ticket': ticket})


# Eliminar ticket (solo accesible por Jefe de Obra o Jefe de Bodega)
@login_required
@user_passes_test(lambda u: has_role_id(u, JEFE_OBRA) or has_role_id(u, JEFE_BODEGA), login_url='/access_denied/')
def eliminar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    return redirect('lista_tickets')


# Vista para alertas de stock (solo accesible por Administrador de Obra)
@login_required
@user_passes_test(lambda u: has_role_id(u, ADMINISTRADOR_OBRA), login_url='/access_denied/')
def stock_alerts_view(request):
    alertas_stock = Material.objects.filter(cantidad_disponible__lt=models.F('stock_minimo'))
    return render(request, 'ReportsView/alertas.html', {'alertas_stock': alertas_stock})


# Vista de reportes (solo accesible por Administradores de Obra)
@login_required
@user_passes_test(lambda u: has_role_id(u, ADMINISTRADOR_OBRA), login_url='/access_denied/')
def reports_view(request):
    reportes = []  # Aquí podrías cargar los reportes desde la base de datos
    return render(request, 'ReportsView/reports.html', {'reportes': reportes})


# Crear usuario
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('home')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'usuarios/create_user.html', {'form': form})


# Cerrar sesión y redirigir al login
def custom_logout_view(request):
    logout(request)
    return redirect('login')


# Vista de acceso denegado
def access_denied_view(request):
    return render(request, 'errors/access_denied.html')


# Crear roles predeterminados
def create_roles(request):
    roles = [
        {'id': ADMINISTRADOR_SISTEMA, 'name': 'Administrador de sistema'},
        {'id': ADMINISTRADOR_OBRA, 'name': 'Administrador de obra'},
        {'id': JEFE_OBRA, 'name': 'Jefe de obra'},
        {'id': CAPATAZ, 'name': 'Capataz'},
        {'id': JEFE_BODEGA, 'name': 'Jefe de Bodega'},
    ]
    
    for role_data in roles:
        Role.objects.get_or_create(id=role_data['id'], defaults={'name': role_data['name']})
    
    return redirect('home')
