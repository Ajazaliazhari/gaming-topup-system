from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('topup.urls')),         # API routes
    path('', include('topup.urls')),             # Add this to allow /dashboard/
]
