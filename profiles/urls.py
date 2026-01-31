from django.urls import path
from .views import (
    home_view,
    profile_view, 
    profile_update_view, 
    questionnaire_view, 
    recommendations_view, 
    interest_questionnaire_view,
    add_academic_result_view,
    delete_academic_result,
    update_academic_result,
    job_offer_list_view,
    job_detail_view,
    apply_for_offer,  

)
from . import views

app_name = 'profiles'

urlpatterns = [
    
    path('', home_view, name='home'),
    
    path('profile/', views.profile_view, name='profile-detail'),
    path('profile/update/', views.profile_update_view, name='profile-update'),
    

    path('profile/public/<int:profile_id>/', views.public_profile_detail_view, name='profile-detail-public'),

    path('questionnaire/', views.questionnaire_view, name='questionnaire'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    

    path('academic-results/add/', views.add_academic_result_view, name='add-academic-result'),
    path('academic-results/<int:result_id>/update/', views.update_academic_result, name='update-academic-result'),
    path('academic-results/<int:result_id>/delete/', views.delete_academic_result, name='delete-academic-result'),


    path('offers/', views.job_offer_list_view, name='offer-list'),
    path('offers/<int:job_id>/', views.job_detail_view, name='job-detail'),
    path('offers/<int:job_id>/apply/', views.apply_for_offer, name='offer-apply'),
]
