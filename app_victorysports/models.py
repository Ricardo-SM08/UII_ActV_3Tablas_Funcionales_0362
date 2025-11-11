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