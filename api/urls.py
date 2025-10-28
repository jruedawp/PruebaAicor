from django.urls import path
from .views import HelloAPI
from .views import Prueba
from .views import InicioSesion
from .views import PerfilAPI
from .views import ProductListAPI
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from .views_auth import RegisterView
urlpatterns = [
    path('hello/', HelloAPI.as_view(), name='hello'),
    path('prueba/', Prueba.as_view(), name = 'prueba'),
    path('inicio/', InicioSesion.as_view(), name='inicio'),
    path('perfil/', PerfilAPI.as_view(), name='perfil'),
    path('productos/', ProductListAPI.as_view(), name='productos_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register')
]
