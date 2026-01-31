# user/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, user_redirect_view

# Le namespace est défini dans config/urls.py, mais app_name est une bonne pratique.
app_name = 'user'

urlpatterns = [
    # URL pour l'inscription
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # URL pour la redirection après connexion
    path('redirect/', user_redirect_view, name='login-redirect'),

    # URLs d'authentification fournies par Django
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path(
        'password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', success_url='done/'), 
        name='password_reset'
    ),
    path(
        'password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', success_url='/accounts/reset/done/'), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
]
