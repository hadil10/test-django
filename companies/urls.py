from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [

    path('dashboard/', views.company_dashboard, name='dashboard'),
   
    path('offer/<int:offer_id>/applicants/', views.offer_applicants_view, name='offer-applicants'),

    path('offers/create/', views.create_job_offer, name='offer-create'),
    

    path('offers/<int:offer_id>/update/', views.update_job_offer, name='offer-update'),
    

    path('offers/<int:offer_id>/delete/', views.delete_job_offer, name='offer-delete'),
]
