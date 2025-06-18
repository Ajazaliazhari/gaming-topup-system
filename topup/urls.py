from django.urls import path
from .views import TopUpAPIView, DashboardView 

urlpatterns = [
    path('topup/', TopUpAPIView.as_view(), name='topup-api'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

