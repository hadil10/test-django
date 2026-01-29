from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('user.urls', namespace='user')),
    path('company/', include('companies.urls', namespace='companies')),
    path('', include('profiles.urls', namespace='profiles')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
