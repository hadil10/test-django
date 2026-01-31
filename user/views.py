from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import login

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        """
        Cette méthode est appelée UNIQUEMENT si le formulaire est valide.
        """
        user = form.save()
        login(self.request, user)
        return redirect('home')
def user_redirect_view(request):
   
    if hasattr(request.user, 'company_profile'):
        return redirect('companies:dashboard') 
    
    elif hasattr(request.user, 'profile'):
        return redirect('profiles:profile-detail')
   
    return redirect('profiles:home')