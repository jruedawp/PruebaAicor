from django.urls import path
from .views import HelloAPI
from .views import Prueba
from .views import InicioSesion
from .views import PerfilAPI

urlpatterns = [
    path('hello/', HelloAPI.as_view(), name='hello'),
    path('prueba/', Prueba.as_view(), name = 'prueba'),
    path('inicio/', InicioSesion.as_view(), name='inicio'),
    path('perfil/', PerfilAPI.as_view(), name='perfil')
]
