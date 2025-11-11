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