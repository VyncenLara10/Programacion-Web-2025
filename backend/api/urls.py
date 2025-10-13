from django.urls import path
from .views import HealthCheckView, HideSecretView, RevealSecretView, StatsView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('hide/', HideSecretView.as_view(), name='hide-secret'),
    path('reveal/<str:key>/', RevealSecretView.as_view(), name='reveal-secret'),
    path('stats/', StatsView.as_view(), name='stats'),
]