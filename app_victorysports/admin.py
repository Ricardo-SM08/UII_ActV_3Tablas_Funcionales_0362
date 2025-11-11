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