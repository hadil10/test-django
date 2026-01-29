# profiles/urls.py

from django.urls import path
# --- IMPORTS CORRIGÉS ---
# On importe les vues en utilisant leurs VRAIS NOMS (en snake_case)
from .views import (
    profile_view, 
    profile_update_view, 
    questionnaire_view, 
    recommendations_view, 
    job_detail_view,
    # JobMarketListView n'existe probablement pas, nous le retirons pour l'instant
)

app_name = 'profiles'

urlpatterns = [
    # --- URLs CORRIGÉES ---
    # On utilise directement les noms des fonctions, sans .as_view()
    
    path('profile/', profile_view, name='profile-detail'),
    path('profile/update/', profile_update_view, name='profile-update'),
    path('questionnaire/', questionnaire_view, name='questionnaire'),
    path('recommendations/', recommendations_view, name='recommendations'),
    
    # URLs liées aux métiers (vues par l'étudiant)
    # path('jobs/', JobMarketListView.as_view(), name='job-market'), # On commente cette ligne pour l'instant
    path('job/<int:job_id>/', job_detail_view, name='job-detail'),
]
