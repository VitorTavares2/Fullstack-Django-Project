from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from cart.models import Order
import json


@method_decorator(staff_member_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "crm/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Métricas básicas
        context['total_revenue'] = (
            Order.objects
            .filter(status="delivered")
            .aggregate(total=Sum("final_amount"))['total'] or 0
        )

        context['total_orders'] = Order.objects.count()

        context['average_ticket'] = (
            Order.objects
            .filter(status="delivered")
            .aggregate(avg=Avg("final_amount"))['avg'] or 0
        )

        context['total_customers'] = (
            Order.objects
            .filter(status="delivered")
            .values('user')
            .distinct()
            .count()
        )

        # ChartJS - Renda Mensal
        revenue_by_month = (
            Order.objects
            .filter(status="delivered")
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Sum('final_amount'))
            .order_by('-month')[:6]
        )

        context['revenue_labels'] = json.dumps(
            [item['month'].strftime('%b') for item in revenue_by_month]
        )
        context['revenue_data'] = json.dumps(
            [float(item['total']) for item in revenue_by_month]
        )

        # ChartJS - Status dos pedidos
        orders_by_status = (
            Order.objects
            .values('status')
            .annotate(count=Count('id'))
        )

        status_map = {
            'processing': 'Processing',
            'shipped': 'Shipping',
            'delivered': 'Delivered',
            'cancelled': 'Cancelled'
        }

        status_labels = []
        status_counts = []

        for item in orders_by_status:
            status_labels.append(status_map.get(item['status'], item['status']))
            status_counts.append(item['count'])

        context['orders_labels'] = json.dumps(status_labels)
        context['orders_data'] = json.dumps(status_counts)

        return context
