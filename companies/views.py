from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction # Pour assurer l'intégrité des données
from .forms import CompanyUserForm, CompanyProfileForm, JobForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied # Pour la sécurité
from .models import Company
from django.contrib import messages # Pour afficher des messages à l'utilisateur
from profiles.models import Job
@transaction.atomic # Garantit que tout réussit, ou tout échoue.
def company_signup_view(request):
    if request.method == 'POST':
        user_form = CompanyUserForm(request.POST)
        profile_form = CompanyProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # 1. Crée l'objet utilisateur mais ne le sauvegarde pas encore en base de données
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            # On définit ce type d'utilisateur comme "entreprise"
            user.user_type = 'company' 
            user.save()

            # 2. Crée l'objet profil entreprise
            company_profile = profile_form.save(commit=False)
            company_profile.user = user  # Lie le profil à l'utilisateur fraîchement créé
            company_profile.save()

            # Redirige vers une page de succès ou de connexion
            return redirect('company_signup_success') # Nous créerons cette page
    else:
        user_form = CompanyUserForm()
        profile_form = CompanyProfileForm()
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'companies/signup.html', context)

# Vue simple pour la page de succès
def company_signup_success_view(request):
    return render(request, 'companies/signup_success.html')
@login_required
def company_dashboard_view(request):
    # 1. Vérifier que l'utilisateur est bien de type 'company'
    if request.user.user_type != 'company':
        # Si ce n'est pas une entreprise, on lève une erreur d'autorisation
        raise PermissionDenied

    # 2. Récupérer le profil de l'entreprise lié à cet utilisateur
    # On utilise un try/except au cas où le profil n'existerait pas, bien que ce soit peu probable
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
         # Cette situation est anormale, on pourrait rediriger ou afficher une erreur
        return redirect('home') 

    context = {
        'company': company
    }
    
    return render(request, 'companies/dashboard.html', context)

@login_required
def job_create_view(request):
    if request.user.user_type != 'company' or not request.user.company_profile.is_approved:
        raise PermissionDenied

    company = request.user.company_profile
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company  # On lie le poste à l'entreprise
            job.save()
            form.save_m2m()  

            messages.success(request, f"La fiche de poste '{job.title}' a été créée avec succès !")
            # Si le formulaire est valide, on quitte la fonction en redirigeant
            return redirect('company_dashboard')
    else:
        # Si ce n'est pas une requête POST, on crée un formulaire vide.
        form = JobForm()
    context = {
        'form': form
    }
    return render(request, 'companies/job_form.html', context)
@login_required
def job_list_view(request):
    # Sécurité : Seules les entreprises peuvent voir cette page
    if request.user.user_type != 'company':
        raise PermissionDenied

    job_postings = request.user.company_profile.job_postings.all().order_by('-created_at')

    context = {
        'job_postings': job_postings
    }
    return render(request, 'companies/job_list.html', context)

@login_required
def job_update_view(request, job_id):
    # Récupère le poste et vérifie qu'il appartient bien à l'entreprise connectée
    job = get_object_or_404(Job, id=job_id, company=request.user.company_profile)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"La fiche de poste '{job.title}' a été mise à jour.")
            return redirect('job_list')
    else:
        form = JobForm(instance=job)

    context = {
        'form': form,
        'is_editing': True
    }
    return render(request, 'companies/job_form.html', context)
@login_required
def job_delete_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company_profile)
    
    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f"La fiche de poste '{job_title}' a été supprimée.")
        return redirect('job_list')
    context = {
        'job': job
    }
    return render(request, 'companies/job_comfirm_delete.html', context)