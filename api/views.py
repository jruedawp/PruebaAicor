import os
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Product,CartItem, Order, OrderItem
from .serializers import  CartItemSerializer, ProductSerializer, OrderSerializer


#INICIO DE SESION GOOGLE
User = get_user_model()

class InicioSesion(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_token_str = request.data.get('id_token')

        if not id_token_str:
            return Response({'error': 'id_token es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') #Obtenemos el CLIENT_ID de las variables de entorno
            print("CLIENT_ID:", CLIENT_ID)
            idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), CLIENT_ID) #conectamos con googlecloud

            #Si el correo no está verificado lanzamos error
            if idinfo.get('email_verified') is not True: 
                return Response({'error': 'El email no está verificado por Google'}, status=status.HTTP_400_BAD_REQUEST)
            
            #Obtenemos las credenciales del cliente
            email = idinfo.get('email')
            name = idinfo.get('name')
            if name == None: name = ''
            google_user_id = idinfo.get('sub')
            
            #Busca un user con este mail y si existe lo devuelve, sino lo crea
            user, created = User.objects.get_or_create(email=email, defaults={ 
                'username': email.split('@')[0],
                'first_name': name.split(' ')[0] if name else '',
                'last_name': ' '.join(name.split(' ')[1:]) if name and len(name.split(' ')) > 1 else '',
            })

            # Genera tokens JWT 
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)


            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            # token inválido
            return Response({'error': 'Token inválido', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Error en el servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#GET EL PERFIL GOOGLE
class PerfilAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

#LISTA DE PRODUCTOS
class ProductListAPI(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        qs = Product.objects.all().order_by('name')
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#CARRITO
class CartAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    #Obtener articulos del carrito
    def get(self, request, pk=None):
        if pk:
            try:
                item = CartItem.objects.get(id=pk, user=request.user)
                return Response(CartItemSerializer(item).data)
            except CartItem.DoesNotExist:
                return Response({'error': 'No encontrado'}, status=404)
        else:
            items = CartItem.objects.filter(user=request.user)
            return Response(CartItemSerializer(items, many=True).data)

     #Añadir articulo al carrito
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            item, created = CartItem.objects.get_or_create(
                user=request.user, product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                item.quantity += quantity
                item.save()
            return Response(CartItemSerializer(item).data, status=201)
        return Response(serializer.errors, status=400)

    #Borrar articulo del carrito
    def delete(self, request, pk=None):
        if not pk:
            return Response({'error': 'Debes indicar el ID del item'}, status=400)
        try:
            item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item no encontrado'}, status=404)

        n = request.query_params.get('n')
        if n:
            n = int(n)
            if item.quantity > n:
                item.quantity -= n
                item.save()
                return Response(status=204)
        item.delete()
        return Response(status=204)


#PEDIDOS
class OrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    #Devuelve pedidos
    def get(self, request, pk=None):
        if pk:
            try:
                order = Order.objects.get(id=pk, user=request.user)
            except Order.DoesNotExist:
                return Response({'error': 'Pedido no encontrado'}, status=404)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=200)
        else:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=200)
        
    #Crear un nuevo pedido
    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'error': 'El carrito está vacío'}, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=user, total=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal=item.product.price * item.quantity
            )

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=201)
    
    #Cambiar estado del pedido
    def patch(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)
        
        new_status = request.data.get('status')
        if new_status not in ['pendiente', 'aceptado', 'cancelado', 'enviado']:
            return Response({'error': 'Estado no válido'}, status=400)
        
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data, status=200)


