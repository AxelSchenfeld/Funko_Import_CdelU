from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# Obtener nombre y apellido concatenados
class Usuario(models.Model):  #!CRUD 
    idUsuario= models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    rol = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.idUsuario} - {self.nombre}'

#Que no haya mas de 2 colecciones con el mismo nombre
class Coleccion(models.Model): #!CRUD
    idColeccion = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100) 

    def __str__(self):
        return self.nombre
 

#calcular el total del carrito
#que no haya mas de 2 carritos con el mismo usuario
class carrito(models.Model): #!CRUD
    idCarrito = models.BigAutoField(primary_key=True)
    total = models.FloatField(validators=[MinValueValidator(0)])
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.idCarrito} - {self.total}'

#Generar automaricamente codigos de descuento
#Que el descuento se aplique al carrito y cuando termine la validez del descuento vuelva al precio original
#Que no haya mas de 2 descuentos al mismo carrito
#Que todos los codigos de descuento sean distintos
class Descuento(models.Model): #!CRUD
    idDescuento = models.AutoField(primary_key=True)
    codigoDescuento = models.CharField(max_length=50, unique=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField() 
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)]) 
    
    def __str__(self):
        return self.codigoDescuento
    
 #que 2 productos no tengan el mismo numero si pertenecen a la misma coleccion
 #reducir stock al hacer compra
class Producto(models.Model): #!CRUD
    idProducto = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField(validators=[MinValueValidator(1)])
    nombreEdicion = models.CharField(max_length=100, null=True)
    esEspecial = models.BooleanField(default=False)
    descripcion = models.CharField(max_length=255)
    brilla = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]) #! agregar en forms
    cantidadDisp = models.IntegerField(validators=[MinValueValidator(0)])  
    URLImagen = models.CharField(max_length=2083)
    idColeccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

#que se aplique la promocion al precio del producto y cuando termine la promocion vuelva al precio original
#Que no haya mas de 2 promociones activas al mismo producto al mismo tiempo
class Promocion(models.Model): #!CRUD
    id_promocion = models.AutoField(primary_key=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)]) #! agregar en forms
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField() 
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    def __str__(self):
        return f'Promocion {self.id_promocion} - {self.porcentaje}%'

#Actualizar stock de producto ingresado
class IngresoStock(models.Model):
    idStock = models.AutoField(primary_key=True)
    cantidadIngresa = models.IntegerField( validators=[MinValueValidator(1)])
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ingreso de stock {self.idStock} - {self.cantidadIngresa}'


class PeticionProducto(models.Model):
    id_peticion = models.AutoField(primary_key=True)
    peticion = models.TextField(max_length=500)
    correo = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=15)
    fechapedido = models.DateField()
    id_Usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def clean(self):
        if self.fechapedido <= timezone.now().date():
            raise ValidationError("La fecha del pedido debe ser posterior a la fecha actual.")
        
        super().clean()

#Al poner una reseña y comentario se tiene que verificar si el usuario compro el producto y si no hizo ya una reseña
#Para ese producto
class ResenaComentario(models.Model): #!CRUD
    idResenaComentario = models.AutoField(primary_key=True)
    resena = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.CharField(max_length=500)
    idUsuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    idProducto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    def __str__(self):
        return f'Reseña {self.idResenaComentario} - {self.resena}'


class Pregunta(models.Model): #!CRUD
    id_pregunta = models.AutoField(primary_key=True)
    pregunta = models.TextField(max_length=255)
    respuesta = models.TextField(max_length=255, null=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    id_Usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f'Pregunta {self.id_pregunta} - {self.pregunta}'

class CarritoDescuento(models.Model):
    idCarritoDescuento = models.AutoField(primary_key=True)
    idCarrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    idDescuento = models.ForeignKey('Descuento', on_delete=models.CASCADE)

    def __str__(self):
        return f'CarritoDescuento {self.idCarritoDescuento} - {self.idCarrito} - {self.idDescuento}'

#generar total en al factura
class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    pago_total = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    forma_pago = models.CharField(max_length=50) #!INUTIL
    fecha_venta = models.DateField()
    id_Usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f'Factura {self.id_factura} - {self.fecha_venta}'

class LineaFactura(models.Model):
    idLineaFactura = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    idProducto = models.ForeignKey('Producto', on_delete=models.CASCADE)    
    idFactura = models.ForeignKey('Factura', on_delete=models.CASCADE)

    def __str__(self):
        return f'LineaFactura {self.idLineaFactura} - {self.cantidad}'

class FacturaDescuento(models.Model):
    idFacturaDescuento = models.AutoField(primary_key=True)
    idDescuento = models.ForeignKey('Descuento', on_delete=models.CASCADE)
    idFactura = models.ForeignKey('Factura', on_delete=models.CASCADE)

    def __str__(self):
        return f'FacturaDescuento {self.idFacturaDescuento} - {self.idDescuento} - {self.idFactura}'

#verificar que no esta el producto 2 veces para el mismo carrito
class ProductoCarrito(models.Model):
    id_producto_carrito = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    id_carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)

    def __str__(self):
        return f'Producto Carrito {self.id_producto_carrito} - {self.cantidad} x {self.precio}'

class CodigoSeguimiento(models.Model): #?CRUD despues vemos
    codigo = models.CharField(max_length=50, unique=True)
    idFactura = models.ForeignKey('Factura', on_delete=models.CASCADE)

    def __str__(self):
        return f'Codigo Seguimiento {self.codigo} - {self.idFactura}'
