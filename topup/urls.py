from django.urls import path
from .views import TopUpAPIView, analytics_dashboard

urlpatterns = [
    # API Endpoint
    path('topup/', TopUpAPIView.as_view(), name='topup_api'),

    # Dashboard View
    path('dashboard/', analytics_dashboard, name='analytics_dashboard'),
]

