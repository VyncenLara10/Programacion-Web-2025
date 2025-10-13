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

# Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


def generate_unique_key():
    """Generate a unique key that doesn't exist in Redis"""
    while True:
        key = secrets.token_urlsafe(16)
        if not redis_client.exists(key):
            return key


class HealthCheckView(APIView):
    """
    Health check endpoint to verify API and Redis connectivity
    """
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
    Store a secret and return a unique key
    POST /api/hide/
    """
    @swagger_auto_schema(
        operation_description="Hide a secret message and get a unique key",
        request_body=SecretSerializer,
        responses={
            201: openapi.Response(
                description="Secret stored successfully",
                examples={
                    "application/json": {
                        "key": "abc123xyz",
                        "message": "Secret stored successfully"
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
                {'error': 'Secret cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Generate unique key
            key = generate_unique_key()
            
            # Store in Redis with 24 hour expiration
            redis_client.setex(
                key,
                timedelta(hours=24),
                secret_text
            )
            
            return Response({
                'key': key,
                'message': 'Secret stored successfully',
                'expires_in': '24 hours'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to store secret: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RevealSecretView(APIView):
    """
    Reveal a secret and delete it immediately
    GET /api/reveal/<key>/
    """
    @swagger_auto_schema(
        operation_description="Reveal a secret message using its key (one-time use)",
        responses={
            200: openapi.Response(
                description="Secret revealed successfully",
                examples={
                    "application/json": {
                        "secret": "Your secret message",
                        "message": "Secret revealed and deleted"
                    }
                }
            ),
            404: "Secret not found or already revealed",
            500: "Internal Server Error"
        }
    )
    def get(self, request, key):
        try:
            # Get the secret
            secret = redis_client.get(key)
            
            if secret is None:
                return Response({
                    'error': 'Secret not found or already revealed',
                    'message': 'This secret may have already been viewed or never existed'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Delete the key immediately after retrieving
            redis_client.delete(key)
            
            return Response({
                'secret': secret,
                'message': 'Secret revealed and permanently deleted'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to reveal secret: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatsView(APIView):
    """
    Get statistics about stored secrets
    GET /api/stats/
    """
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