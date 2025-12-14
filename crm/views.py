from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(staff_member_required, name = "dispatch")
class DashboardView(TemplateView):
    template_name = "crm/dashboard.html"