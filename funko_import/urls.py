from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
# router.register(r'Coleccion', views.ColeccionView, 'Coleccion')

router.register(r'usuarios', views.UsuarioView, basename='usuario')
router.register(r'colecciones', views.ColeccionView, basename='coleccion')
router.register(r'carritos', views.CarritoView, basename='carrito')
router.register(r'descuentos', views.DescuentoView, basename='descuento')
router.register(r'productos', views.ProductoView, basename='producto')
router.register(r'promociones', views.PromocionView, basename='promocion')
router.register(r'resenas', views.resenaComentarioView, basename='resena')
router.register(r'preguntas', views.preguntaView, basename='pregunta')
router.register(r'ediciones', views.EdicionView, basename='edicion')

urlpatterns = [
    path('', include(router.urls)),  # Rutas del router bajo el prefijo 'api/auth/'
    path('auth/google-login/', views.google_login, name='google_login'),  # Ahora estÃ¡ bajo 'api/auth/google-login/'
    path("process_payment/", views.process_payment, name="process_payment"),
    path('auth/completar-perfil/', views.completar_perfil, name='completar_perfil'),
]