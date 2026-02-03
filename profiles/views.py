from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseForbidden, HttpResponse
from .forms import ProfileUpdateForm, AcademicResultForm

from .models import (
    Profile, 
    Skill, 
    Interest, 
    UserSkillEvaluation, 
    UserInterestEvaluation, 
    AcademicResult
 )
from companies.models import JobOffer, Application
from .recommender import get_job_recommendations
def home_view(request):
    return render(request, 'home.html', {})

@login_required 
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {'profile': profile}
    return render(request, 'profiles/profile_detail.html', context)
    
@login_required
def profile_update_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # ... (sauvegarde du profil) ...

            # Gestion des compétences
            skills_str = form.cleaned_data.get('skills', '')
            # LA CORRECTION EST ICI : on filtre les chaînes vides
            skill_names = [name.strip() for name in skills_str.split(',') if name.strip()]
            
            updated_profile.skills.clear()
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(name__iexact=name.lower())
                updated_profile.skills.add(skill)

            # Gestion des centres d'intérêt
            interests_str = form.cleaned_data.get('interests', '')
            # LA CORRECTION EST ICI : on filtre les chaînes vides
            interest_names = [name.strip() for name in interests_str.split(',') if name.strip()]

            updated_profile.interests.clear()
            for name in interest_names:
                interest, created = Interest.objects.get_or_create(name__iexact=name.lower())
                updated_profile.interests.add(interest)
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profiles:profile-detail')
    else:
        skills_str = ", ".join([skill.name for skill in profile.skills.all()])
      
        interests_str = ", ".join([interest.name for interest in profile.interests.all()])
        
        form = ProfileUpdateForm(
            instance=profile, 
            initial={'skills': skills_str, 'interests': interests_str}
        )

    context = {'form': form}
    return render(request, 'profiles/profile_form.html', context)



@login_required
def questionnaire_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    all_skills = Skill.objects.all()
    all_interests = Interest.objects.all()

    if request.method == 'POST':
        for skill in all_skills:
            level = request.POST.get(f'skill_{skill.id}')
            if level:
                UserSkillEvaluation.objects.update_or_create(
                    profile=profile, skill=skill, defaults={'level': int(level)}
                )
        for interest in all_interests:
            level = request.POST.get(f'interest_{interest.id}')
            if level:
                UserInterestEvaluation.objects.update_or_create(
                    profile=profile, interest=interest, defaults={'level': int(level)}
                )
        messages.success(request, 'Votre questionnaire a été enregistré avec succès !')
        return redirect('profiles:profile-detail')

    context = {
        'all_skills': all_skills,
        'all_interests': all_interests,
        'existing_skill_evals': {eval.skill.id: eval.level for eval in profile.skill_evaluations.all()},
        'existing_interest_evals': {eval.interest.id: eval.level for eval in profile.interest_evaluations.all()},
        'skill_levels': UserSkillEvaluation.LEVEL_CHOICES,
        'interest_levels': UserInterestEvaluation.INTEREST_CHOICES,
    }
    return render(request, 'profiles/questionnaire.html', context)
@login_required
def recommendations_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    recommendations = get_job_recommendations(profile)
    
    context = {
        'recommendations': recommendations
    }
    
    return render(request, 'profiles/recommendations.html', context)
@login_required
def job_detail_view(request, job_id):
    
    offer = get_object_or_404(JobOffer, id=job_id, is_active=True)
    has_applied = False

    
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
     
        student_profile = request.user.profile
        has_applied = Application.objects.filter(
            student=student_profile,
            job_offer=offer
        ).exists()

    
    context = {
        'offer': offer,
        'has_applied': has_applied, 
    }
    return render(request, 'profiles/job_detail.html', context)
@login_required
def interest_questionnaire_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    interests = Interest.objects.all()

    if request.method == 'POST':
        for interest in interests:
            level = request.POST.get(f'interest_{interest.id}')
            if level:

                UserInterestEvaluation.objects.update_or_create(
                    profile=profile,
                    interest=interest,
                    defaults={'level': int(level)}
                )

        return redirect('recommendations')

    existing_evaluations = {eval.interest.id: eval.level for eval in profile.interest_evaluations.all()}
    
    context = {
        'interests': interests,
        'existing_evaluations': existing_evaluations,
    }
    return render(request, 'profiles/interest_questionnaire.html', context)
@login_required
def redirect_on_login_view(request):
    if request.user.user_type == 'company':
        return redirect('companies:dashboard')
    else:
        return redirect('home')
@login_required
def add_academic_result_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = AcademicResultForm(request.POST)
        if form.is_valid():
            try:
                result = form.save(commit=False)
                result.profile = profile
                result.save()
                messages.success(request, 'Résultat académique ajouté avec succès !')
                return redirect('/profile/')
            except IntegrityError:
                messages.error(request, 'Vous avez deja ajouté un résultat académique pour cette matière.')
    else:
        form = AcademicResultForm()
    existing_results = profile.academic_results.all().order_by('-year', 'subject')    

    context = {
        'form': form,
        'results': existing_results
    }
    return render(request, 'profiles/academic_results.html', context)
@login_required
def delete_academic_result(request, result_id):
    result = get_object_or_404(AcademicResult, id=result_id)

    if result.profile.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce résultat.")
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Résultat académique supprimé avec succès !')
    return redirect('/profile/')
@login_required
def update_academic_result(request, result_id):
    result = get_object_or_404(AcademicResult, id=result_id)

    if request.method == 'POST':
        form = AcademicResultForm(request.POST, instance=result)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Résultat académique mis à jour avec succès !')
                return redirect('/profile/')
            except IntegrityError:
                messages.error(request, 'Vous avez déjà un résultat académique pour cette matière et cette année.')
    else:
        form = AcademicResultForm(instance=result)

    context = {
        'form': form,
        'result_id': result_id
    }
    return render(request, 'profiles/academic_result_form.html', context)

# =======================================================
#  POUR LISTER TOUTES LES OFFRES D'EMPLOI
# =======================================================
@login_required
def job_offer_list_view(request):
    """
    Affiche la liste de toutes les offres d'emploi actives.
    """
    offers = JobOffer.objects.filter(is_active=True)
    
    context = {
        'offers': offers
    }
    return render(request, 'profiles/offers_list.html', context)
# =======================================================
#  POUR LE DÉTAIL D'UNE OFFRE D'EMPLOI
# =======================================================
@login_required
def job_offer_detail_view(request, offer_id):
    """
    Affiche les détails d'une offre d'emploi spécifique.
    """
    offer = get_object_or_404(JobOffer, id=offer_id, is_active=True)
    
    context = {
        'offer': offer
    }
    
    return render(request, 'profiles/offer_detail.html', context)   

# =======================================================
#  POUR POSTULER À UNE OFFRE
# =======================================================
@login_required
def apply_for_offer(request, job_id):
    if request.user.user_type != 'student':
        messages.error(request, "Seuls les étudiants peuvent postuler aux offres.")
        return redirect('profiles:home')

    if request.method == 'POST':
        job_offer = get_object_or_404(JobOffer, id=job_id)
        student_profile = get_object_or_404(Profile, user=request.user)

        try:

            Application.objects.create(
                student=student_profile, 
                job_offer=job_offer
            )
            messages.success(request, f"Votre candidature pour '{job_offer.title}' a été envoyée avec succès !")
        
        except IntegrityError:

            messages.warning(request, "Vous avez déjà postulé à cette offre.")


        return redirect('profiles:job-detail', job_id=job_id)
    return redirect('profiles:job-detail', job_id=job_id)
# =======================================================
#  LE PROFIL PUBLIC (consultable par les entreprises)
# =======================================================
@login_required
def public_profile_detail_view(request, profile_id):
    """
    Affiche une version publique du profil d'un étudiant.
    Accessible par les entreprises qui ont reçu une candidature.
    """

    if not hasattr(request.user, 'company_profile'):
        return HttpResponseForbidden("Accès réservé aux entreprises.")

 
    profile = get_object_or_404(Profile, id=profile_id)
    
  
    context = {
        'profile': profile,
    }

    return render(request, 'profiles/profile_detail.html', context)