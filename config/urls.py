# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclut toutes les URLs de l'application 'user' (signup, login, logout, etc.)
    # sous le préfixe /accounts/. Nous lui donnons un namespace 'user'.
    path('accounts/', include('user.urls', namespace='user')),

    # Inclut toutes les URLs de l'application 'companies'
    # sous le préfixe /company/
    path('company/', include('companies.urls', namespace='companies')),

    # Inclut toutes les URLs de l'application 'profiles'
    # SANS préfixe. C'est le cœur de notre site.
    path('', include('profiles.urls', namespace='profiles')),
]

# Ne touchez pas à cette partie, elle est correcte.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
