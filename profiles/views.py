# profiles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Pour restreindre l'accès
from .models import Profile
from django.contrib import messages
from .forms import ProfileUpdateForm
from .models import Profile, Skill, Interest, UserSkillEvaluation, UserInterestEvaluation, Job
from .recommender import get_job_recommendations 

def home_view(request):
    """
    Cette vue affiche la page d'accueil.
    """
    # La fonction render prend la requête, le nom du template, et un contexte (vide pour l'instant)
    # et renvoie une page HTML.
    return render(request, 'home.html', {})

@login_required # Ce décorateur bloque l'accès si l'utilisateur n'est pas connecté
def profile_view(request):
    """
    Affiche le profil de l'utilisateur actuellement connecté.
    """
    # On récupère l'objet Profile associé à l'utilisateur de la requête (request.user).
    # get_object_or_404 est une bonne pratique : si le profil n'existe pas, il renvoie une erreur 404.
    profile = get_object_or_404(Profile, user=request.user)
    
    # On passe l'objet 'profile' au template dans un dictionnaire de contexte.
    context = {
        'profile': profile
    }
    
    return render(request, 'profiles/profile_detail.html', context)
    
@login_required
def profile_update_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Si le formulaire est soumis, on le peuple avec les données POST ET l'instance du profil à modifier
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save() # La magie du ModelForm : sauvegarde les modifications
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('/profile/') # Redirige vers la page de profil
    else:
        # Si c'est une requête GET, on affiche le formulaire pré-rempli avec les données actuelles
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'profiles/profile_form.html', context)

@login_required
def questionnaire_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    # Récupère toutes les compétences et tous les intérêts
    all_skills = Skill.objects.all()
    all_interests = Interest.objects.all()

    if request.method == 'POST':
        # Le formulaire a été soumis, traitons les données
        for skill in all_skills:
            # Le nom du champ dans le HTML sera 'skill_LEVEL_ID' (ex: 'skill_1')
            level = request.POST.get(f'skill_{skill.id}')
            if level:
                # On utilise update_or_create pour créer ou mettre à jour l'évaluation
                UserSkillEvaluation.objects.update_or_create(
                    profile=profile,
                    skill=skill,
                    defaults={'level': int(level)}
                )
        
        for interest in all_interests:
            level = request.POST.get(f'interest_{interest.id}')
            if level:
                UserInterestEvaluation.objects.update_or_create(
                    profile=profile,
                    interest=interest,
                    defaults={'level': int(level)}
                )
        
        messages.success(request, 'Votre questionnaire a été enregistré avec succès !')
        return redirect('/profile/') # Redirige vers le profil pour voir le résultat (que nous ajouterons plus tard)

    existing_skill_evals = {eval.skill.id: eval.level for eval in profile.skill_evaluations.all()}
    existing_interest_evals = {eval.interest.id: eval.level for eval in profile.interest_evaluations.all()}

    context = {
        'all_skills': all_skills,
        'all_interests': all_interests,
        'existing_skill_evals': existing_skill_evals,
        'existing_interest_evals': existing_interest_evals,
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
    """
    Affiche les détails d'un métier spécifique.
    """
    job = get_object_or_404(Job, id=job_id)
    
    context = {
        'job': job
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
                # Crée ou met à jour l'évaluation pour cet intérêt
                UserInterestEvaluation.objects.update_or_create(
                    profile=profile,
                    interest=interest,
                    defaults={'level': int(level)}
                )
        # Redirige vers la page des recommandations pour voir les résultats mis à jour
        return redirect('recommendations')

    # Récupère les évaluations existantes pour pré-remplir le formulaire
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
    else: # Par défaut, on considère que c'est un étudiant
        return redirect('home')
