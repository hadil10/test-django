from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Company, JobOffer, Application
from .forms import JobOfferForm 
from profiles.models import Skill


def company_required(view_func ):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'company_profile'):
            return HttpResponseForbidden("Accès réservé aux profils d'entreprise.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# =======================================================
# LE TABLEAU DE BORD DE L'ENTREPRISE (VOTRE OBJECTIF)
# =======================================================
@company_required
def company_dashboard(request):
    """
    Affiche le tableau de bord de l'entreprise avec la liste de ses offres.
    C'est la page principale pour une entreprise.
    """
    company_profile = get_object_or_404(Company, user=request.user)
    job_offers = company_profile.job_offers.all().order_by('-created_at')
    
    context = {
        'company': company_profile,
        'offers': job_offers,
    }
    return render(request, 'companies/dashboard.html', context)

# =======================================================
# LA VUE POUR VOIR LES CANDIDATS (LA PIÈCE MANQUANTE)
# =======================================================
@company_required
def offer_applicants_view(request, offer_id):
    """
    Affiche la liste de tous les étudiants qui ont postulé à une offre spécifique.
    """
    # On récupère l'offre, en s'assurant qu'elle appartient bien à l'entreprise connectée.
    offer = get_object_or_404(JobOffer, id=offer_id, company__user=request.user)
    
    # On récupère toutes les candidatures pour cette offre.
    applicants = Application.objects.filter(job_offer=offer).select_related('student__user').order_by('-applied_at')
    
    context = {
        'offer': offer,
        'applicants': applicants,
    }
    return render(request, 'companies/offer_applicants.html', context)

# =======================================================
# GESTION DES OFFRES D'EMPLOI (Création)
# =======================================================
@login_required
def create_job_offer(request):
    if request.user.user_type != 'company':
        return redirect('profiles:home')
    company_profile = get_object_or_404(Company, user=request.user)

    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            new_offer = form.save(commit=False)
            new_offer.company = company_profile
            new_offer.save()
            
            skills_str = request.POST.get('required_skills', '')
            skill_names = [name.strip() for name in skills_str.split(',') if name.strip()]
            
            new_offer.required_skills.clear()
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(name__iexact=name.lower())
                new_offer.required_skills.add(skill)
            messages.success(request, "L'offre d'emploi a été créée avec succès (compétences non traitées).")
            return redirect('companies:dashboard')
    else:
        form = JobOfferForm()
    context = {'form': form, 'form_title': "Créer une nouvelle offre"}
    return render(request, 'companies/job_offer_form.html', context)


@login_required
def update_job_offer(request, offer_id):
    if request.user.user_type != 'company':
        return redirect('profiles:home')
    offer = get_object_or_404(JobOffer, id=offer_id, company__user=request.user)

    if request.method == 'POST':
        form = JobOfferForm(request.POST, instance=offer)
        if form.is_valid():
            updated_offer = form.save()
            
            skills_str = request.POST.get('required_skills', '')
            skill_names = [name.strip() for name in skills_str.split(',') if name.strip()]
            
            updated_offer.required_skills.clear()
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(name__iexact=name.lower())
                updated_offer.required_skills.add(skill)
            messages.success(request, "L'offre d'emploi a été mise à jour avec succès (compétences non traitées).")
            return redirect('companies:dashboard')
    else:
        skills_str = ", ".join([skill.name for skill in offer.required_skills.all()])
        form = JobOfferForm(instance=offer, initial={'required_skills': skills_str})
    context = {'form': form, 'form_title': f"Modifier l'offre : {offer.title}"}
    return render(request, 'companies/job_offer_form.html', context)
# SUPPRIMER UNE OFFRE D'EMPLOI
# =======================================================
@company_required
def delete_job_offer(request, offer_id):
    """
    Supprime une offre d'emploi.
    """
    offer = get_object_or_404(JobOffer, id=offer_id, company__user=request.user)
    
    if request.method == 'POST':
        offer_title = offer.title
        offer.delete()
        messages.success(request, f"L'offre '{offer_title}' a été supprimée avec succès.")
        return redirect('companies:dashboard')
    
    context = {'offer': offer}
    return render(request, 'companies/confirm_delete_offer.html', context)
