# companies/urls.py

from django.urls import path
# --- IMPORTS CORRIGÉS ---
# On importe les vues en utilisant leurs VRAIS NOMS (en snake_case)
from .views import (
    company_dashboard_view, 
    job_list_view, 
    job_create_view, 
    job_update_view, 
    job_delete_view
)

app_name = 'companies'

urlpatterns = [
    # --- URLs CORRIGÉES ---
    # On utilise directement les noms des fonctions, sans .as_view()
    
    path('dashboard/', company_dashboard_view, name='dashboard'),
    
    # URLs pour la gestion des fiches de poste par l'entreprise
    path('jobs/', job_list_view, name='job-list'),
    path('jobs/create/', job_create_view, name='job-create'),
    path('jobs/<int:job_id>/update/', job_update_view, name='job-update'),
    path('jobs/<int:job_id>/delete/', job_delete_view, name='job-delete'),
]
