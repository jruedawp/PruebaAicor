from django.urls import path
from .views import PerfilAPI, InicioSesion, ProductListAPI, CartAPI, OrderAPI
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from .views_auth import RegisterView
urlpatterns = [
    path('inicio/', InicioSesion.as_view(), name='inicio'),
    path('perfil/', PerfilAPI.as_view(), name='perfil'),
    path('productos/', ProductListAPI.as_view(), name='productos_list'),
    path('productos/<int:pk>/', ProductListAPI.as_view(), name='producto_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cart/', CartAPI.as_view(), name='cart_list_create'),
    path('cart/<int:pk>/', CartAPI.as_view(), name='cart_detail'),
    path('orders/', OrderAPI.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderAPI.as_view(), name='order_detail'),
    ]
