# user/views.py

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import login

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    # La redirection se fera manuellement, donc success_url n'est pas nécessaire.

    def form_valid(self, form):
        """
        Cette méthode est appelée UNIQUEMENT si le formulaire est valide.
        """
        # 1. On sauvegarde le formulaire pour créer l'utilisateur.
        user = form.save()
        
        # 2. On connecte cet utilisateur à la session actuelle.
        login(self.request, user)
        
        # 3. On redirige manuellement vers la page d'accueil.
        return redirect('home')
