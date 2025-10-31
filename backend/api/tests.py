from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Product, CartItem, Order, OrderItem

User = get_user_model()

class APITestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',  # obligatorio
            email='test@example.com',
            password='test1234'
        )
        self.client = APIClient()
        
        # Autenticar
        self.client.force_authenticate(user=self.user)
        
        # Crear productos de prueba
        self.product1 = Product.objects.create(name='Producto 1', price=10, stock=10)
        self.product2 = Product.objects.create(name='Producto 2', price=20, stock=10)

    
    def test_add_to_cart(self):
        data = {
            'product_id': self.product1.id,
            'quantity': 2
        }

        response = self.client.post('/api/cart/', data, format='json')

        # Comprobaciones
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.product, self.product1)
        self.assertEqual(cart_item.quantity, 2)

    def test_create_order(self):
        # Añadir producto al carrito
        CartItem.objects.create(user=self.user, product=self.product1, quantity=2)
        
        # Crear pedido
        response = self.client.post('/api/orders/', {})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(Order.objects.first().total, 20)  # 2*10
    
    def test_login_jwt(self):
        # No podemos probar login Google real en TDD, pero podemos testear token manual
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)
        self.assertTrue(refresh.access_token)
