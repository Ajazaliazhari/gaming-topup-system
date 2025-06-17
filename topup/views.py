from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction # For atomic operations
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate # For daily aggregation
import datetime

from .models import Game, TopUpProduct, TopUpOrder
from .serializers import TopUpRequestSerializer, TopUpOrderSerializer

class TopUpAPIView(APIView):
    """
    API endpoint for handling gaming top-up requests.
    POST /api/topup/
    """
    def post(self, request, *args, **kwargs):
        serializer = TopUpRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Using transaction.atomic to ensure all database operations succeed or fail together
            try:
                with transaction.atomic():
                    # Retrieve the product instance from the validated data
                    product_instance = serializer.validated_data['product_instance']

                    # Create the TopUpOrder
                    topup_order = TopUpOrder.objects.create(
                        user_email=serializer.validated_data['user_email'],
                        product=product_instance,
                        status=serializer.validated_data['payment_status'] # Initially 'pending'
                    )

                    # Serialize the created TopUpOrder for the response
                    response_serializer = TopUpOrderSerializer(topup_order)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required # Requires user to be logged in
@user_passes_test(lambda u: u.is_staff) # Requires user to be staff
def analytics_dashboard(request):
    """
    View for displaying the analytics dashboard.
    Accessible only to staff users.
    """
    # 1. Top 5 Most Purchased Top-Up Products
    # Annotate with count, order by count descending, select related product and game for efficiency
    top_products = TopUpOrder.objects.filter(status='success') \
        .values('product__name', 'product__game__name') \
        .annotate(purchase_count=Count('product')) \
        .order_by('-purchase_count')[:5]

    # 2. Daily Revenue (last 7 days) from successful orders
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=6) # Inclusive of today

    daily_revenue = TopUpOrder.objects.filter(
        status='success',
        created_at__date__gte=seven_days_ago,
        created_at__date__lte=today
    ) \
    .annotate(date=TruncDate('created_at')) \
    .values('date') \
    .annotate(total_revenue=Sum('product__price')) \
    .order_by('date')

    # Prepare data for easy template rendering (fill in missing dates with 0 revenue)
    revenue_data_map = {item['date']: item['total_revenue'] for item in daily_revenue}
    last_7_days_revenue = []
    for i in range(7):
        current_date = seven_days_ago + datetime.timedelta(days=i)
        last_7_days_revenue.append({
            'date': current_date,
            'total_revenue': revenue_data_map.get(current_date, 0.00)
        })

    # 3. Failed Payment Count (current month)
    current_month_start = today.replace(day=1)
    failed_payments_count = TopUpOrder.objects.filter(
        status='failed',
        created_at__date__gte=current_month_start,
        created_at__date__lte=today # Up to today
    ).count()

    context = {
        'top_products': top_products,
        'daily_revenue': last_7_days_revenue,
        'failed_payments_count': failed_payments_count,
    }

    return render(request, 'dashboard.html', context)

