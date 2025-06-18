from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from topup.models import TopUpOrder
from django.utils import timezone
from django.db.models import Count, Sum
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TopUpOrderSerializer


class TopUpAPIView(APIView):
    def post(self, request):
        serializer = TopUpOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "Top-up order created", "order_id": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(staff_member_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        today = timezone.now().date()
        last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

        top_products = (TopUpOrder.objects
                        .filter(status='success')
                        .values('product__name')
                        .annotate(total=Count('product'))
                        .order_by('-total')[:5])

        daily_revenue = []
        for day in last_7_days:
            revenue = (TopUpOrder.objects
                       .filter(status='success', created_at__date=day)
                       .aggregate(total=Sum('product__price'))['total'] or 0)
            daily_revenue.append({'date': day, 'revenue': revenue})

        now = timezone.now()
        failed_count = TopUpOrder.objects.filter(
            status='failed',
            created_at__month=now.month,
            created_at__year=now.year
        ).count()

        context = {
            'top_products': top_products,
            'daily_revenue': daily_revenue,
            'failed_count': failed_count
        }

        return render(request, 'dashboard.html', context)
