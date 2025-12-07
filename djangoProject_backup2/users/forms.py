from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        required = True,
    )
    last_name = forms.CharField(
        max_length=30,
        required = True,
    )
    username = forms.CharField(
        max_length= 30,
        required = True,
    )

    def save(self,request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.save()
        return user