# user/urls.py

from django.urls import path, include

# --- IMPORTS CORRIGÉS ---

# 1. On importe la vue d'inscription de l'étudiant depuis le fichier local 'user/views.py'.
from .views import SignUpView

# 2. On importe les vues pour l'inscription de l'entreprise en utilisant leurs VRAIS NOMS (en snake_case).
from companies.views import company_signup_view, company_signup_success_view

# 3. On importe la vue de redirection depuis l'application 'profiles'.
from profiles.views import redirect_on_login_view

app_name = 'user'

urlpatterns = [
    # URL pour l'inscription de l'étudiant (c'est une classe, donc on utilise .as_view())
    path('signup/student/', SignUpView.as_view(), name='student-signup'),
    
    # URLs pour l'inscription de l'entreprise (ce sont des fonctions, donc on n'utilise PAS .as_view())
    path('signup/company/', company_signup_view, name='company-signup'),
    path('signup/company/success/', company_signup_success_view, name='company-signup-success'),
    
    # URL pour la redirection après connexion
    path('redirect/', redirect_on_login_view, name='login-redirect'),
    
    # Inclut toutes les URLs d'authentification par défaut de Django
    path('', include('django.contrib.auth.urls')),
]
