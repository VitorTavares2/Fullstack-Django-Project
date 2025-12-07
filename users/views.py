from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class UpdateProfileView(LoginRequiredMixin, View):
    """
    Update user profile information (address, phone, etc.)
    """
    login_url = 'account_login'
    
    def post(self, request):
        profile = request.user.profile
        
        profile.phone = request.POST.get("phone")
        profile.Adress = request.POST.get("Adress")
        profile.ZIPCODE = request.POST.get("ZIPCODE")
        profile.City = request.POST.get("City")
        profile.State = request.POST.get("State")
        
        profile.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect("userSection")