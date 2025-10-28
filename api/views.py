import os
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .models import CartItem
from rest_framework.permissions import AllowAny




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


class ProductListAPI(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        qs = Product.objects.all().order_by('name')
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemListAPI(APIView):
    permission_classes = [AllowAny] 
    def post(self, request, user):
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        if not user_id or not product_id:
            return Response({'error': 'user y product son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )

        
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        
        return Response({
            'user': user.id,
            'product': product.name,
            'quantity': cart_item.quantity,
            'added_at': cart_item.added_at,  # aquí mostramos cuándo se añadió
            'message': 'Item añadido al carrito'
        }, status=status.HTTP_201_CREATED)

#PRUEBAS
class HelloAPI(APIView):
    def get(self, request):
        return Response({'message': '¡Hola, esto es la API de la tienda!'}, status=status.HTTP_200_OK)

class Prueba(APIView):
    def get(self, request, p1 = None, p2 = None):
        p1 = request.query_params.get('p1')
        p2 = request.query_params.get('p2')
        
        if p1 and p2:
            return Response(1)
        if p1:
            return Response(2)
        if p2:
            return Response(3)
        
        return Response(4)