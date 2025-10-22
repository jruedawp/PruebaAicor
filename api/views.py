from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloAPI(APIView):
    def get(self, request):
        return Response({'message': '¡Hola, esto es la API de la tienda!'}, status=status.HTTP_200_OK)
