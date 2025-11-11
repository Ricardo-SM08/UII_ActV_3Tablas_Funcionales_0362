¡Excelente\! Aquí tienes **todos los archivos de código completos** para copiar y pegar directamente en tu proyecto **VictorySports**, cubriendo Proveedores, Productos y las Conexiones (ProductoProveedor).

Asegúrate de haber completado la configuración inicial de carpetas y el entorno virtual antes de pegar estos archivos.

-----

## 1\. Archivos de Configuración de Django

### 📄 `backend_Victorysports/settings.py` (Fragmento Clave)

Asegúrate de que esta línea esté presente en tu lista `INSTALLED_APPS`:

```python
# backend_Victorysports/settings.py (Fragmento)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_victorysports',  # <--- Aplicación principal
]

# ...

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_TZ = True 
```

### 📄 `backend_Victorysports/urls.py`

```python
# backend_Victorysports/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Enlaza todas las rutas de la app a la raíz del proyecto
    path('', include('app_victorysports.urls')), 
]
```

-----

## 2\. Archivos de Lógica de la Aplicación (`app_victorysports/`)

### 📄 `app_victorysports/models.py`

```python
# app_victorysports/models.py

from django.db import models

#--- Modelo para Proveedor ---
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=150, unique=True)
    telefono_empresa = models.CharField(max_length=15)
    email_empresa = models.EmailField(max_length=100)
    pais_origen = models.CharField(max_length=50)
    contacto_principal = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)
    direccion = models.TextField()

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre_empresa

#--- Modelo para Producto ---
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    marca = models.CharField(max_length=100)
    img_url = models.URLField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

# Modelo para Producto Proveedor (Tabla Intermedia/Many-to-Many con Datos Adicionales)
class ProductoProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,
                                 related_name='relaciones_proveedor')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,
                                  related_name='relaciones_producto')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ultima_compra = models.DateField(null=True, blank=True)
    cantidad_comprada = models.IntegerField(default=1)
    referencia_pedido = models.CharField(max_length=50, blank=True, null=True)
    es_proveedor_activo = models.BooleanField(default=True)

    class Meta:
        unique_together = (('producto', 'proveedor'),)
        verbose_name = "Producto por Proveedor"
        verbose_name_plural = "Productos por Proveedores"

    def __str__(self):
        return f"Relación: {self.producto.nombre} - {self.proveedor.nombre_empresa}"
```

### 📄 `app_victorysports/admin.py`

```python
# app_victorysports/admin.py

from django.contrib import admin
from .models import Proveedor, Producto, ProductoProveedor

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id_proveedor', 'nombre_empresa', 'contacto_principal', 'pais_origen', 'fecha_registro')
    search_fields = ('nombre_empresa', 'contacto_principal', 'email_empresa')
    list_filter = ('pais_origen', 'fecha_registro')
    ordering = ('nombre_empresa',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'marca', 'categoria', 'stock', 'precio_unitario')
    search_fields = ('nombre', 'marca', 'categoria')
    list_filter = ('categoria', 'marca', 'stock')
    ordering = ('nombre',)

class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ('producto', 'proveedor', 'precio_compra', 'cantidad_comprada', 'es_proveedor_activo')
    list_filter = ('es_proveedor_activo', 'fecha_ultima_compra')
    search_fields = ('producto__nombre', 'proveedor__nombre_empresa')

admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ProductoProveedor, ProductoProveedorAdmin)
```

### 📄 `app_victorysports/urls.py`

```python
# app_victorysports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rutas Comunes
    path('', views.inicio_victorysports, name='inicio_victorysports'),
    
    # Rutas CRUD Proveedor
    path('proveedores/', views.ver_proveedor, name='ver_proveedor'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:pk>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/realizar_actualizacion/', views.realizar_actualizacion_proveedor, name='realizar_actualizacion_proveedor'),
    path('proveedores/borrar/<int:pk>/', views.borrar_proveedor, name='borrar_proveedor'),

    # Rutas CRUD Producto
    path('productos/', views.ver_producto, name='ver_producto'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/realizar_actualizacion/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
    path('productos/borrar/<int:pk>/', views.borrar_producto, name='borrar_producto'),
    
    # Rutas CRUD ProductoProveedor (Conexión)
    path('conexiones/', views.ver_conexion, name='ver_conexion'),
    path('conexiones/agregar/', views.agregar_conexion, name='agregar_conexion'),
    path('conexiones/actualizar/<int:pk>/', views.actualizar_conexion, name='actualizar_conexion'),
    path('conexiones/realizar_actualizacion/', views.realizar_actualizacion_conexion, name='realizar_actualizacion_conexion'),
    path('conexiones/borrar/<int:pk>/', views.borrar_conexion, name='borrar_conexion'),
]
```

### 📄 `app_victorysports/views.py`

```python
# app_victorysports/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Proveedor, Producto, ProductoProveedor
from django.db import IntegrityError 

# Vista de Inicio
def inicio_victorysports(request):
    return render(request, 'inicio.html') 

# ----------------------
# Funciones CRUD Proveedor
# ----------------------
def agregar_proveedor(request):
    if request.method == 'POST':
        try:
            Proveedor.objects.create(
                nombre_empresa=request.POST.get('nombre_empresa'),
                telefono_empresa=request.POST.get('telefono_empresa'),
                email_empresa=request.POST.get('email_empresa'),
                pais_origen=request.POST.get('pais_origen'),
                contacto_principal=request.POST.get('contacto_principal'),
                direccion=request.POST.get('direccion')
            )
            return redirect(reverse('ver_proveedor'))
        except IntegrityError:
            context = {'error_message': 'Ya existe un proveedor con ese nombre de empresa.'}
            return render(request, 'proveedor/agregar_proveedor.html', context)
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'proveedor/agregar_proveedor.html', context)
    return render(request, 'proveedor/agregar_proveedor.html')

def ver_proveedor(request):
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    context = {'proveedores': proveedores}
    return render(request, 'proveedor/ver_proveedor.html', context)

def actualizar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    context = {'proveedor': proveedor}
    return render(request, 'proveedor/actualizar_proveedor.html', context)

def realizar_actualizacion_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('id_proveedor')
        proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
        try:
            proveedor.nombre_empresa = request.POST.get('nombre_empresa')
            proveedor.telefono_empresa = request.POST.get('telefono_empresa')
            proveedor.email_empresa = request.POST.get('email_empresa')
            proveedor.pais_origen = request.POST.get('pais_origen')
            proveedor.contacto_principal = request.POST.get('contacto_principal')
            proveedor.direccion = request.POST.get('direccion')
            proveedor.save()
            return redirect(reverse('ver_proveedor'))
        except IntegrityError:
            context = {'proveedor': proveedor, 'error_message': 'Ya existe un proveedor con ese nombre de empresa.'}
            return render(request, 'proveedor/actualizar_proveedor.html', context)
        except Exception as e:
            context = {'proveedor': proveedor, 'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'proveedor/actualizar_proveedor.html', context)
    return redirect(reverse('ver_proveedor'))

def borrar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect(reverse('ver_proveedor'))
    context = {'proveedor': proveedor}
    return render(request, 'proveedor/borrar_proveedor.html', context)

# ----------------------
# Funciones CRUD Producto
# ----------------------
def agregar_producto(request):
    if request.method == 'POST':
        try:
            Producto.objects.create(
                nombre=request.POST.get('nombre'),
                precio_unitario=request.POST.get('precio_unitario'),
                stock=request.POST.get('stock'),
                marca=request.POST.get('marca'),
                img_url=request.POST.get('img_url'),
                categoria=request.POST.get('categoria'),
                color=request.POST.get('color')
            )
            return redirect(reverse('ver_producto'))
        except Exception as e:
            context = {'error_message': f'Ocurrió un error al guardar: {e}'}
            return render(request, 'producto/agregar_producto.html', context)
    return render(request, 'producto/agregar_producto.html')

def ver_producto(request):
    productos = Producto.objects.all().order_by('nombre')
    context = {'productos': productos}
    return render(request, 'producto/ver_producto.html', context)

def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    context = {'producto': producto}
    return render(request, 'producto/actualizar_producto.html', context)

def realizar_actualizacion_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id_producto')
        producto = get_object_or_404(Producto, pk=producto_id)
        try:
            producto.nombre = request.POST.get('nombre')
            producto.precio_unitario = request.POST.get('precio_unitario')
            producto.stock = request.POST.get('stock')
            producto.marca = request.POST.get('marca')
            producto.img_url = request.POST.get('img_url')
            producto.categoria = request.POST.get('categoria')
            producto.color = request.POST.get('color')
            producto.save()
            return redirect(reverse('ver_producto'))
        except Exception as e:
            context = {'producto': producto, 'error_message': f'Ocurrió un error al actualizar: {e}'}
            return render(request, 'producto/actualizar_producto.html', context)
    return redirect(reverse('ver_producto'))

def borrar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect(reverse('ver_producto'))
    context = {'producto': producto}
    return render(request, 'producto/borrar_producto.html', context)

# -----------------------------------
# Funciones CRUD ProductoProveedor (Conexión)
# -----------------------------------
def agregar_conexion(request):
    productos = Producto.objects.all().order_by('nombre')
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')

    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            proveedor_id = request.POST.get('proveedor_id')
            
            producto_obj = get_object_or_404(Producto, pk=producto_id)
            proveedor_obj = get_object_or_404(Proveedor, pk=proveedor_id)

            ProductoProveedor.objects.create(
                producto=producto_obj,
                proveedor=proveedor_obj,
                precio_compra=request.POST.get('precio_compra'),
                cantidad_comprada=request.POST.get('cantidad_comprada'),
                fecha_ultima_compra=request.POST.get('fecha_ultima_compra') or None,
                referencia_pedido=request.POST.get('referencia_pedido'),
                es_proveedor_activo=request.POST.get('es_proveedor_activo') == 'on'
            )
            return redirect(reverse('ver_conexion'))
        except IntegrityError:
            context = {
                'productos': productos, 
                'proveedores': proveedores, 
                'error_message': 'Esta conexión entre Producto y Proveedor ya existe.'
            }
            return render(request, 'producto_proveedor/agregar_conexion.html', context)
        except Exception as e:
            context = {
                'productos': productos, 
                'proveedores': proveedores, 
                'error_message': f'Ocurrió un error al guardar: {e}'
            }
            return render(request, 'producto_proveedor/agregar_conexion.html', context)

    context = {'productos': productos, 'proveedores': proveedores}
    return render(request, 'producto_proveedor/agregar_conexion.html', context)

def ver_conexion(request):
    conexiones = ProductoProveedor.objects.all().order_by('producto__nombre', 'proveedor__nombre_empresa')
    context = {'conexiones': conexiones}
    return render(request, 'producto_proveedor/ver_conexion.html', context)

def actualizar_conexion(request, pk):
    conexion = get_object_or_404(ProductoProveedor, pk=pk)
    productos = Producto.objects.all().order_by('nombre')
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    
    context = {'conexion': conexion, 'productos': productos, 'proveedores': proveedores}
    return render(request, 'producto_proveedor/actualizar_conexion.html', context)

def realizar_actualizacion_conexion(request):
    if request.method == 'POST':
        conexion_id = request.POST.get('id_conexion')
        conexion = get_object_or_404(ProductoProveedor, pk=conexion_id)
        productos = Producto.objects.all().order_by('nombre')
        proveedores = Proveedor.objects.all().order_by('nombre_empresa')

        try:
            conexion.precio_compra = request.POST.get('precio_compra')
            conexion.cantidad_comprada = request.POST.get('cantidad_comprada')
            conexion.fecha_ultima_compra = request.POST.get('fecha_ultima_compra') or None
            conexion.referencia_pedido = request.POST.get('referencia_pedido')
            conexion.es_proveedor_activo = request.POST.get('es_proveedor_activo') == 'on' 
            
            conexion.save()
            return redirect(reverse('ver_conexion'))
        except Exception as e:
            context = {
                'conexion': conexion, 
                'productos': productos, 
                'proveedores': proveedores, 
                'error_message': f'Ocurrió un error al actualizar: {e}'
            }
            return render(request, 'producto_proveedor/actualizar_conexion.html', context)

    return redirect(reverse('ver_conexion'))

def borrar_conexion(request, pk):
    conexion = get_object_or_404(ProductoProveedor, pk=pk)
    if request.method == 'POST':
        conexion.delete()
        return redirect(reverse('ver_conexion'))
    context = {'conexion': conexion}
    return render(request, 'producto_proveedor/borrar_conexion.html', context)
```

-----

## 3\. Archivos HTML (Templates)

### 3.1. Base y Navegación

#### 📄 `app_victorysports/templates/base.html`

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}VictorySports Admin{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
    <style>
        body { background-color: #f8f9fa; }
        .navbar { background-color: #4a6fa5 !important; }
        .footer { background-color: #343a40; color: white; }
        html { position: relative; min-height: 100%; }
        body { margin-bottom: 70px; }
    </style>
</head>
<body>
    {% include "header.html" %}
    {% include "navbar.html" %}

    <div class="container mt-4 mb-5">
        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% include "footer.html" %}
</body>
</html>
```

#### 📄 `app_victorysports/templates/header.html`

```html
<header class="py-3 bg-light border-bottom">
    <div class="container d-flex justify-content-center">
        <h5 class="text-secondary mb-0">Administración de Inventario y Proveedores</h5>
    </div>
</header>
```

#### 📄 `app_victorysports/templates/navbar.html`

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
    <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'inicio_victorysports' %}">Sistema de Administración Victorysports</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'inicio_victorysports' %}">Inicio</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="proveedorDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Proveedor
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="proveedorDropdown">
                        <li><a class="dropdown-item" href="{% url 'agregar_proveedor' %}">Agregar Proveedor</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_proveedor' %}">Ver Proveedores</a></li>
                    </ul>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="productosDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Productos
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="productosDropdown">
                        <li><a class="dropdown-item" href="{% url 'agregar_producto' %}">Agregar Producto</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_producto' %}">Ver Producto</a></li>
                        <li><a class="dropdown-item" href="#">Actualizar Producto</a></li>
                        <li><a class="dropdown-item" href="#">Borrar Producto</a></li>
                    </ul>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="conexionDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Producto Proveedor
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="conexionDropdown">
                        <li><a class="dropdown-item" href="{% url 'agregar_conexion' %}">Agregar Conexión</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_conexion' %}">Ver Conexiones</a></li>
                    </ul>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="categoriasDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Categorías
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="categoriasDropdown">
                        <li><a class="dropdown-item" href="#">Agregar Categoria</a></li>
                        <li><a class="dropdown-item" href="#">Ver Categoria</a></li>
                        <li><a class="dropdown-item" href="#">Actualizar Categoria</a></li>
                        <li><a class="dropdown-item" href="#">Borrar Categoria</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

#### 📄 `app_victorysports/templates/footer.html`

```html
{% load static %}
<footer class="footer mt-auto py-3 bg-dark fixed-bottom">
    <div class="container text-center">
        <span class="text-light">
            &copy; Derechos de Autor Victorysports {{ "now"|date:"Y" }} |
            Fecha del Sistema: {{ "now"|date:"d/m/Y H:i:s" }} |
            Creado por Tec. Ricardo Santiago, Cbtis 128
        </span>
    </div>
</footer>
```

#### 📄 `app_victorysports/templates/inicio.html`

```html
{% extends "base.html" %}
{% load static %}

{% block title %}Inicio - VictorySports{% endblock %}

{% block content %}
<div class="p-5 mb-4 bg-light rounded-3 text-center">
    <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold text-primary">Bienvenido al Sistema de Administración VictorySports</h1>
        <p class="col-md-8 fs-4 mx-auto">
            Este sistema permite gestionar de manera eficiente los **Proveedores**, **Productos** y sus **Conexiones**
            de la empresa VictorySports, incluyendo operaciones de Creación, Lectura, Actualización y Eliminación (CRUD).
        </p>
        <hr class="my-4">
        <p class="fs-6 text-muted">Desarrollado en Python con el framework Django.</p>
    </div>
</div>

<div class="row">
    <div class="col-lg-12 text-center">
        <img src="https://via.placeholder.com/800x300?text=Imagen+VictorySports" class="img-fluid rounded shadow" alt="Imagen representativa de VictorySports">
    </div>
</div>
{% endblock content %}
```

-----

### 3.2. Templates de Proveedor (`app_victorysports/templates/proveedor/`)

#### 📄 `agregar_proveedor.html`

```html
{% extends "base.html" %}

{% block title %}Agregar Proveedor{% endblock %}

{% block content %}
<h2 class="mb-4 text-primary">Agregar Nuevo Proveedor</h2>

{% if error_message %}
    <div class="alert alert-danger" role="alert">{{ error_message }}</div>
{% endif %}

<form method="POST" action="{% url 'agregar_proveedor' %}">
    {% csrf_token %}
    <div class="card shadow-sm">
        <div class="card-body">
            <div class="mb-3">
                <label for="nombre_empresa" class="form-label">Nombre de la Empresa</label>
                <input type="text" class="form-control" id="nombre_empresa" name="nombre_empresa" required>
            </div>
            <div class="mb-3">
                <label for="contacto_principal" class="form-label">Contacto Principal</label>
                <input type="text" class="form-control" id="contacto_principal" name="contacto_principal" required>
            </div>
            <div class="mb-3">
                <label for="telefono_empresa" class="form-label">Teléfono</label>
                <input type="tel" class="form-control" id="telefono_empresa" name="telefono_empresa" required>
            </div>
            <div class="mb-3">
                <label for="email_empresa" class="form-label">Email</label>
                <input type="email" class="form-control" id="email_empresa" name="email_empresa" required>
            </div>
            <div class="mb-3">
                <label for="pais_origen" class="form-label">País de Origen</label>
                <input type="text" class="form-control" id="pais_origen" name="pais_origen" required>
            </div>
            <div class="mb-3">
                <label for="direccion" class="form-label">Dirección</label>
                <textarea class="form-control" id="direccion" name="direccion" rows="3" required></textarea>
            </div>
        </div>
        <div class="card-footer text-end">
            <button type="submit" class="btn btn-success">Guardar Proveedor</button>
            <a href="{% url 'ver_proveedor' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </div>
</form>
{% endblock content %}
```

#### 📄 `ver_proveedor.html`

```html
{% extends "base.html" %}

{% block title %}Ver Proveedores{% endblock %}

{% block content %}
<h2 class="mb-4 text-primary">Lista de Proveedores</h2>

<div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Nombre Empresa</th>
                <th>Contacto</th>
                <th>Teléfono</th>
                <th>Email</th>
                <th>País</th>
                <th>Registro</th>
                <th class="text-center">Acciones</th>
            </tr>
        </thead>
        <tbody>
            {% for proveedor in proveedores %}
            <tr>
                <td>{{ proveedor.id_proveedor }}</td>
                <td>{{ proveedor.nombre_empresa }}</td>
                <td>{{ proveedor.contacto_principal }}</td>
                <td>{{ proveedor.telefono_empresa }}</td>
                <td>{{ proveedor.email_empresa }}</td>
                <td>{{ proveedor.pais_origen }}</td>
                <td>{{ proveedor.fecha_registro|date:"d/m/Y" }}</td>
                <td class="text-center">
                    <a href="#" class="btn btn-sm btn-info" title="Ver Detalle">Ver</a> 
                    <a href="{% url 'actualizar_proveedor' pk=proveedor.id_proveedor %}" class="btn btn-sm btn-warning" title="Editar">Editar</a>
                    <a href="{% url 'borrar_proveedor' pk=proveedor.id_proveedor %}" class="btn btn-sm btn-danger" title="Borrar">Borrar</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="8" class="text-center">No hay proveedores registrados.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<div class="text-end mt-3">
    <a href="{% url 'agregar_proveedor' %}" class="btn btn-primary">Agregar Nuevo Proveedor</a>
</div>
{% endblock content %}
```

#### 📄 `actualizar_proveedor.html`

```html
{% extends "base.html" %}

{% block title %}Actualizar Proveedor: {{ proveedor.nombre_empresa }}{% endblock %}

{% block content %}
<h2 class="mb-4 text-warning">Actualizar Proveedor</h2>

{% if error_message %}
    <div class="alert alert-danger" role="alert">{{ error_message }}</div>
{% endif %}

<form method="POST" action="{% url 'realizar_actualizacion_proveedor' %}">
    {% csrf_token %}
    <input type="hidden" name="id_proveedor" value="{{ proveedor.id_proveedor }}">
    
    <div class="card shadow-sm">
        <div class="card-body">
            <div class="mb-3">
                <label for="nombre_empresa" class="form-label">Nombre de la Empresa</label>
                <input type="text" class="form-control" id="nombre_empresa" name="nombre_empresa" value="{{ proveedor.nombre_empresa }}" required>
            </div>
            <div class="mb-3">
                <label for="contacto_principal" class="form-label">Contacto Principal</label>
                <input type="text" class="form-control" id="contacto_principal" name="contacto_principal" value="{{ proveedor.contacto_principal }}" required>
            </div>
            <div class="mb-3">
                <label for="telefono_empresa" class="form-label">Teléfono</label>
                <input type="tel" class="form-control" id="telefono_empresa" name="telefono_empresa" value="{{ proveedor.telefono_empresa }}" required>
            </div>
            <div class="mb-3">
                <label for="email_empresa" class="form-label">Email</label>
                <input type="email" class="form-control" id="email_empresa" name="email_empresa" value="{{ proveedor.email_empresa }}" required>
            </div>
            <div class="mb-3">
                <label for="pais_origen" class="form-label">País de Origen</label>
                <input type="text" class="form-control" id="pais_origen" name="pais_origen" value="{{ proveedor.pais_origen }}" required>
            </div>
            <div class="mb-3">
                <label for="direccion" class="form-label">Dirección</label>
                <textarea class="form-control" id="direccion" name="direccion" rows="3" required>{{ proveedor.direccion }}</textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">Fecha de Registro</label>
                <p class="form-control-static">{{ proveedor.fecha_registro|date:"d/m/Y" }}</p>
                <small class="text-muted">La fecha de registro no se puede modificar.</small>
            </div>
        </div>
        <div class="card-footer text-end">
            <button type="submit" class="btn btn-warning">Actualizar Proveedor</button>
            <a href="{% url 'ver_proveedor' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </div>
</form>
{% endblock content %}
```

#### 📄 `borrar_proveedor.html`

```html
{% extends "base.html" %}

{% block title %}Borrar Proveedor{% endblock %}

{% block content %}
<div class="alert alert-danger" role="alert">
    <h4 class="alert-heading">¡Advertencia de Eliminación!</h4>
    <p>Estás a punto de eliminar al proveedor **{{ proveedor.nombre_empresa }}** (ID: {{ proveedor.id_proveedor }}). Esta acción es irreversible.</p>
    <hr>
    <p class="mb-0">¿Estás absolutamente seguro que deseas continuar?</p>
</div>

<div class="card shadow-sm">
    <div class="card-body">
        <p><strong>Detalles del Proveedor:</strong></p>
        <ul>
            <li>**Empresa:** {{ proveedor.nombre_empresa }}</li>
            <li>**Contacto:** {{ proveedor.contacto_principal }}</li>
            <li>**Teléfono:** {{ proveedor.telefono_empresa }}</li>
        </ul>

        <form method="POST" action="{% url 'borrar_proveedor' pk=proveedor.id_proveedor %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger btn-lg">Sí, Eliminar Permanentemente</button>
            <a href="{% url 'ver_proveedor' %}" class="btn btn-secondary btn-lg">No, Volver a la Lista</a>
        </form>
    </div>
</div>
{% endblock content %}
```

-----

### 3.3. Templates de Producto (`app_victorysports/templates/producto/`)

#### 📄 `agregar_producto.html`

```html
{% extends "base.html" %}

{% block title %}Agregar Producto{% endblock %}

{% block content %}
<h2 class="mb-4 text-primary">Agregar Nuevo Producto</h2>

{% if error_message %}
    <div class="alert alert-danger" role="alert">{{ error_message }}</div>
{% endif %}

<form method="POST" action="{% url 'agregar_producto' %}">
    {% csrf_token %}
    <div class="card shadow-sm">
        <div class="card-body">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="nombre" class="form-label">Nombre del Producto</label>
                    <input type="text" class="form-control" id="nombre" name="nombre" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="marca" class="form-label">Marca</label>
                    <input type="text" class="form-control" id="marca" name="marca" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="precio_unitario" class="form-label">Precio Unitario ($)</label>
                    <input type="number" step="0.01" class="form-control" id="precio_unitario" name="precio_unitario" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="stock" class="form-label">Stock</label>
                    <input type="number" class="form-control" id="stock" name="stock" value="0" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="categoria" class="form-label">Categoría</label>
                    <input type="text" class="form-control" id="categoria" name="categoria" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="color" class="form-label">Color</label>
                    <input type="text" class="form-control" id="color" name="color" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="img_url" class="form-label">URL de Imagen (Opcional)</label>
                    <input type="url" class="form-control" id="img_url" name="img_url">
                </div>
            </div>
        </div>
        <div class="card-footer text-end">
            <button type="submit" class="btn btn-success">Guardar Producto</button>
            <a href="{% url 'ver_producto' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </div>
</form>
{% endblock content %}
```

#### 📄 `ver_producto.html`

```html
{% extends "base.html" %}

{% block title %}Ver Productos{% endblock %}

{% block content %}
<h2 class="mb-4 text-primary">Lista de Productos</h2>

<div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Marca</th>
                <th>Categoría</th>
                <th>Precio</th>
                <th>Stock</th>
                <th class="text-center">Acciones</th>
            </tr>
        </thead>
        <tbody>
            {% for producto in productos %}
            <tr>
                <td>{{ producto.id_producto }}</td>
                <td>{{ producto.nombre }}</td>
                <td>{{ producto.marca }}</td>
                <td>{{ producto.categoria }}</td>
                <td>${{ producto.precio_unitario|floatformat:2 }}</td>
                <td>{{ producto.stock }}</td>
                <td class="text-center">
                    <a href="#" class="btn btn-sm btn-info" title="Ver Detalle">Ver</a> 
                    <a href="{% url 'actualizar_producto' pk=producto.id_producto %}" class="btn btn-sm btn-warning" title="Editar">Editar</a>
                    <a href="{% url 'borrar_producto' pk=producto.id_producto %}" class="btn btn-sm btn-danger" title="Borrar">Borrar</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="7" class="text-center">No hay productos registrados.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<div class="text-end mt-3">
    <a href="{% url 'agregar_producto' %}" class="btn btn-primary">Agregar Nuevo Producto</a>
</div>
{% endblock content %}
```

#### 📄 `actualizar_producto.html`

```html
{% extends "base.html" %}

{% block title %}Actualizar Producto: {{ producto.nombre }}{% endblock %}

{% block content %}
<h2 class="mb-4 text-warning">Actualizar Producto</h2>

{% if error_message %}
    <div class="alert alert-danger" role="alert">{{ error_message }}</div>
{% endif %}

<form method="POST" action="{% url 'realizar_actualizacion_producto' %}">
    {% csrf_token %}
    <input type="hidden" name="id_producto" value="{{ producto.id_producto }}">
    
    <div class="card shadow-sm">
        <div class="card-body">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="nombre" class="form-label">Nombre del Producto</label>
                    <input type="text" class="form-control" id="nombre" name="nombre" value="{{ producto.nombre }}" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="marca" class="form-label">Marca</label>
                    <input type="text" class="form-control" id="marca" name="marca" value="{{ producto.marca }}" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="precio_unitario" class="form-label">Precio Unitario ($)</label>
                    <input type="number" step="0.01" class="form-control" id="precio_unitario" name="precio_unitario" value="{{ producto.precio_unitario }}" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="stock" class="form-label">Stock</label>
                    <input type="number" class="form-control" id="stock" name="stock" value="{{ producto.stock }}" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="categoria" class="form-label">Categoría</label>
                    <input type="text" class="form-control" id="categoria" name="categoria" value="{{ producto.categoria }}" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="color" class="form-label">Color</label>
                    <input type="text" class="form-control" id="color" name="color" value="{{ producto.color }}" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="img_url" class="form-label">URL de Imagen (Opcional)</label>
                    <input type="url" class="form-control" id="img_url" name="img_url" value="{{ producto.img_url|default:'' }}">
                </div>
            </div>
        </div>
        <div class="card-footer text-end">
            <button type="submit" class="btn btn-warning">Actualizar Producto</button>
            <a href="{% url 'ver_producto' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </div>
</form>
{% endblock content %}
```

#### 📄 `borrar_producto.html`

```html
{% extends "base.html" %}

{% block title %}Borrar Producto{% endblock %}

{% block content %}
<div class="alert alert-danger" role="alert">
    <h4 class="alert-heading">¡Advertencia de Eliminación!</h4>
    <p>Estás a punto de eliminar el producto **{{ producto.nombre }}** (ID: {{ producto.id_producto }}). Esta acción es irreversible.</p>
    <hr>
    <p class="mb-0">¿Estás absolutamente seguro que deseas continuar?</p>
</div>

<div class="card shadow-sm">
    <div class="card-body">
        <p><strong>Detalles del Producto:</strong></p>
        <ul>
            <li>**Nombre:** {{ producto.nombre }}</li>
            <li>**Marca:** {{ producto.marca }}</li>
            <li>**Categoría:** {{ producto.categoria }}</li>
            <li>**Precio:** ${{ producto.precio_unitario }}</li>
        </ul>

        <form method="POST" action="{% url 'borrar_producto' pk=producto.id_producto %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger btn-lg">Sí, Eliminar Permanentemente</button>
            <a href="{% url 'ver_producto' %}" class="btn btn-secondary btn-lg">No, Volver a la Lista</a>
        </form>
    </div>
</div>
{% endblock content %}
```

-----

### 3.4. Templates de ProductoProveedor (`app_victorysports/templates/producto_proveedor/`)

#### 📄 `agregar_conexion.html`

```html
{% extends "base.html" %}

{% block title %}Agregar Conexión (Producto Proveedor){% endblock %}

{% block content %}
<h2 class="mb-4 text-primary">Agregar Nueva Conexión Producto - Proveedor</h2>

{% if error_message %}
    <div class="alert alert-danger" role="alert">{{ error_message }}</div>
{% endif %}

<form method="POST" action="{% url 'agregar_conexion' %}">
    {% csrf_token %}
    <div class="card shadow-sm">
        <div class="card-header bg-secondary text-white">Datos de la Relación</div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="producto_id" class="form-label">Producto</label>
                    <select class="form-select" id="producto_id" name="producto_id" required>
                        <option value="">Seleccione un producto</option>
                        {% for producto in productos %}
                            <option value="{{ producto.id_producto }}">{{ producto.nombre }} ({{ producto.marca }})</option>
                        {% empty %}
                            <option value="" disabled>No hay productos disponibles.</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="proveedor_id" class="form-label">Proveedor</label>
                    <select class="form-select" id="proveedor_id" name="proveedor_id" required>
                        <option value="">Seleccione un proveedor</option>
                        {% for proveedor in proveedores %}
                            <option value="{{ proveedor.id_proveedor }}">{{ proveedor.nombre_empresa }}</option>
                        {% empty %}
                            <option value="" disabled>No hay proveedores disponibles.</option>
                        {% endfor %}
                    </select>
                </div>
            </div>

            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="precio_compra" class="form-label">Precio de Compra ($)</label>
                    <input type="number" step="0.01" class="form-control" id="precio_compra" name="precio_compra" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="cantidad_comprada" class="form-label">Cantidad Comprada</label>
                    <input type="number" class="form-control" id="cantidad_comprada" name="cantidad_comprada" value="1" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="fecha_ultima_compra" class="form-label">Fecha Última Compra (Opcional)</label>
                    <input type="date" class="form-control" id="fecha_ultima_compra" name="fecha_ultima_compra">
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="referencia_pedido" class="form-label">Referencia del Pedido (Opcional)</label>
                    <input type="text" class="form-control" id="referencia_pedido" name="referencia_pedido">
                </div>
                <div class="col-md-6 mb-3 form-check d-flex align-items-center pt-4">
                    <input class="form-check-input" type="checkbox" id="es_proveedor_activo" name="es_proveedor_activo" checked>
                    <label class="form-check-label ms-2" for="es_proveedor_activo">
                        ¿Es Proveedor Activo para este Producto?
                    </label>
                </div>
            </div>
        </div>
        <div class="card-footer text-end">
            <button type="submit" class="btn btn-success">Crear Conexión</button>
            <a href="{% url 'ver_conexion' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </div>
</form>
{% endblock content %}
```

#### 📄 `ver_conexion.html`

```html
{% extends "base.html" %}

{% block title %}Ver Conexiones (Producto Proveedor){% endblock %}

{% block content %}
<h2 class="mb-4 text-primary">Lista de Conexiones Producto - Proveedor</h2>

<div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Proveedor</th>
                <th>Precio Compra</th>
                <th>Cantidad</th>
                <th>Activo</th>
                <th>Última Compra</th>
                <th class="text-center">Acciones</th>
            </tr>
        </thead>
        <tbody>
            {% for con in conexiones %}
            <tr>
                <td>{{ con.pk }}</td>
                <td>{{ con.producto.nombre }} ({{ con.producto.marca }})</td>
                <td>{{ con.proveedor.nombre_empresa }}</td>
                <td>${{ con.precio_compra|floatformat:2 }}</td>
                <td>{{ con.cantidad_comprada }}</td>
                <td>
                    {% if con.es_proveedor_activo %}
                        <span class="badge bg-success">Sí</span>
                    {% else %}
                        <span class="badge bg-danger">No</span>
                    {% endif %}
                </td>
                <td>{{ con.fecha_ultima_compra|default:"N/A" }}</td>
                <td class="text-center">
                    <a href="#" class="btn btn-sm btn-info" title="Ver Detalle">Ver</a> 
                    <a href="{% url 'actualizar_conexion' pk=con.pk %}" class="btn btn-sm btn-warning" title="Editar">Editar</a>
                    <a href="{% url 'borrar_conexion' pk=con.pk %}" class="btn btn-sm btn-danger" title="Borrar">Borrar</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="8" class="text-center">No hay conexiones Producto - Proveedor registradas.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<div class="text-end mt-3">
    <a href="{% url 'agregar_conexion' %}" class="btn btn-primary">Agregar Nueva Conexión</a>
</div>
{% endblock content %}
```

#### 📄 `actualizar_conexion.html`

```html
{% extends "base.html" %}

{% block title %}Actualizar Conexión{% endblock %}

{% block content %}
<h2 class="mb-4 text-warning">Actualizar Conexión: {{ conexion.producto.nombre }} - {{ conexion.proveedor.nombre_empresa }}</h2>

{% if error_message %}
    <div class="alert alert-danger" role="alert">{{ error_message }}</div>
{% endif %}

<form method="POST" action="{% url 'realizar_actualizacion_conexion' %}">
    {% csrf_token %}
    <input type="hidden" name="id_conexion" value="{{ conexion.pk }}">
    
    <div class="card shadow-sm">
        <div class="card-header bg-secondary text-white">Datos de la Relación</div>
        <div class="card-body">
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Producto</label>
                    <input type="text" class="form-control" value="{{ conexion.producto.nombre }} ({{ conexion.producto.marca }})" disabled>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Proveedor</label>
                    <input type="text" class="form-control" value="{{ conexion.proveedor.nombre_empresa }}" disabled>
                </div>
            </div>

            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="precio_compra" class="form-label">Precio de Compra ($)</label>
                    <input type="number" step="0.01" class="form-control" id="precio_compra" name="precio_compra" value="{{ conexion.precio_compra }}" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="cantidad_comprada" class="form-label">Cantidad Comprada</label>
                    <input type="number" class="form-control" id="cantidad_comprada" name="cantidad_comprada" value="{{ conexion.cantidad_comprada }}" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="fecha_ultima_compra" class="form-label">Fecha Última Compra (Opcional)</label>
                    <input type="date" class="form-control" id="fecha_ultima_compra" name="fecha_ultima_compra" value="{{ conexion.fecha_ultima_compra|date:'Y-m-d'|default:'' }}">
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="referencia_pedido" class="form-label">Referencia del Pedido (Opcional)</label>
                    <input type="text" class="form-control" id="referencia_pedido" name="referencia_pedido" value="{{ conexion.referencia_pedido|default:'' }}">
                </div>
                <div class="col-md-6 mb-3 form-check d-flex align-items-center pt-4">
                    <input class="form-check-input" type="checkbox" id="es_proveedor_activo" name="es_proveedor_activo" {% if conexion.es_proveedor_activo %}checked{% endif %}>
                    <label class="form-check-label ms-2" for="es_proveedor_activo">
                        ¿Es Proveedor Activo para este Producto?
                    </label>
                </div>
            </div>
        </div>
        <div class="card-footer text-end">
            <button type="submit" class="btn btn-warning">Actualizar Conexión</button>
            <a href="{% url 'ver_conexion' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </div>
</form>
{% endblock content %}
```

#### 📄 `borrar_conexion.html`

```html
{% extends "base.html" %}

{% block title %}Borrar Conexión{% endblock %}

{% block content %}
<div class="alert alert-danger" role="alert">
    <h4 class="alert-heading">¡Advertencia de Eliminación!</h4>
    <p>Estás a punto de eliminar la conexión entre **{{ conexion.producto.nombre }}** y **{{ conexion.proveedor.nombre_empresa }}** (ID: {{ conexion.pk }}). Esta acción es irreversible y afectará la relación de inventario/compra.</p>
    <hr>
    <p class="mb-0">¿Estás absolutamente seguro que deseas continuar?</p>
</div>

<div class="card shadow-sm">
    <div class="card-body">
        <p><strong>Detalles de la Conexión:</strong></p>
        <ul>
            <li>**Producto:** {{ conexion.producto.nombre }} ({{ conexion.producto.marca }})</li>
            <li>**Proveedor:** {{ conexion.proveedor.nombre_empresa }}</li>
            <li>**Precio de Compra:** ${{ conexion.precio_compra }}</li>
        </ul>

        <form method="POST" action="{% url 'borrar_conexion' pk=conexion.pk %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger btn-lg">Sí, Eliminar Permanentemente</button>
            <a href="{% url 'ver_conexion' %}" class="btn btn-secondary btn-lg">No, Volver a la Lista</a>
        </form>
    </div>
</div>
{% endblock content %}
```

