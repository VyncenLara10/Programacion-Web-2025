from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import redis
import secrets
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import SecretSerializer

# Redis conexion
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


def generate_unique_key():
    """Genera una sola clave unica que no exista en redis"""
    while True:
        key = secrets.token_urlsafe(16)
        if not redis_client.exists(key):
            return key


class HealthCheckView(APIView):
    def get(self, request):
        try:
            redis_client.ping()
            return Response({
                'status': 'healthy',
                'redis': 'connected',
                'message': 'All systems operational'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'redis': 'disconnected',
                'error': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class HideSecretView(APIView):
    """
    guarda el secreto y devuelve la clave
    POST /api/hide/
    """
    @swagger_auto_schema(
        operation_description="Escondiendo mensaje en clave unica",
        request_body=SecretSerializer,
        responses={
            201: openapi.Response(
                description="Secreto oculto correctamente",
                examples={
                    "application/json": {
                        "key": "abc123xyz",
                        "message": "Secreto oculto correctamente"
                    }
                }
            ),
            400: "Bad Request - Secret is required",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        serializer = SecretSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        secret_text = serializer.validated_data['secret']
        
        if not secret_text.strip():
            return Response(
                {'error': 'Secreto no puede estar vacio'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Genera la clave unica 
            key = generate_unique_key()
            
            # Se almacena en redis por 24 horas si pasan chipilin
            redis_client.setex(
                key,
                timedelta(hours=24),
                secret_text
            )
            
            return Response({
                'key': key,
                'message': 'Secreto oculto correctamente',
                'expires_in': '24 horas'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Fallo al revelar: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RevealSecretView(APIView):
    """
    REvela el secreto y lo borra de redis 
    GET /api/reveal/<key>/
    """
    @swagger_auto_schema(
        operation_description="Reveal a secret message using its key (one-time use)",
        responses={
            200: openapi.Response(
                description="Secreto revelado correctamente",
                examples={
                    "application/json": {
                        "secret": "Your secret message",
                        "message": "secreo revelado y eliminado"
                    }
                }
            ),
            404: "Clave no se encuentra o ya se uso",
            500: "Error de servidor"
        }
    )
    def get(self, request, key):
        try:
            # Obtiene el secreto
            secret = redis_client.get(key)
            
            if secret is None:
                return Response({
                    'error': 'Clave no se encuentra o ya se uso',
                    'message': 'secreto ya se vio o no existio'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Borra la llave luego de ser usada
            redis_client.delete(key)
            
            return Response({
                'secret': secret,
                'message': 'Secreto revelado y eliminado permanentemente'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to reveal secret: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatsView(APIView):
    @swagger_auto_schema(
        operation_description="Get current statistics about active secrets",
        responses={
            200: openapi.Response(
                description="Statistics retrieved successfully",
                examples={
                    "application/json": {
                        "active_secrets": 42,
                        "database_size": 42
                    }
                }
            )
        }
    )
    def get(self, request):
        try:
            total_keys = redis_client.dbsize()
            return Response({
                'active_secrets': total_keys,
                'database_size': total_keys,
                'status': 'operational'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )