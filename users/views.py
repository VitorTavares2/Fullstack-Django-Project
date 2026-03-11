from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile


class UpdateProfileView(LoginRequiredMixin, View):
    """
    Update user profile information (address, phone, etc.)
    FIXED: Added form validation, error handling, and proper POST handling
    """
    login_url = 'account_login'
    
    def post(self, request):
        # FIXED: Use form for validation instead of direct assignment
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found. Please contact support.")
            return redirect("userSection")
        
        form = ProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            # FIXED: Proper form handling
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("userSection")
        else:
            # FIXED: Show validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("userSection")
    
    def get(self, request):
        # FIXED: Redirect GET requests to profile page
        messages.info(request, "Use the form on this page to update your profile")
        return redirect("userSection")