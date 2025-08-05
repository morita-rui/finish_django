from django.contrib.auth.forms import UserCreationForm   
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django import forms

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')     
    template_name = 'accounts/signup.html'
    template_email = 'accounts/signup.html'