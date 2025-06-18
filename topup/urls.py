from django.urls import path
from .views import TopUpAPIView, analytics_dashboard

urlpatterns = [
    path('topup/', TopUpAPIView.as_view(), name='topup-api'),
    path('dashboard/', analytics_dashboard, name='dashboard'),  # must match view name
]
