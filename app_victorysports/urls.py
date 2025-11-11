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