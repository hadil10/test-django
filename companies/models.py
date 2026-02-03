# companies/models.py

from django.db import models
from django.conf import settings

# PAS D'IMPORT DEPUIS profiles.models ICI POUR ÉVITER LA BOUCLE

def company_logo_path(instance, filename):
    if instance.user:
        return f'company_logos/{instance.user.id}/{filename}'
    return f'company_logos/default/{filename}'

class Company(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='company_profile'
    )
    name = models.CharField(max_length=255, unique=True, help_text="Le nom officiel de l'entreprise")
    description = models.TextField(blank=True, help_text="Description de l'entreprise, sa culture, etc.")
    website = models.URLField(blank=True, help_text="Site web de l'entreprise")
    industry = models.CharField(max_length=100, blank=True, verbose_name="Secteur d'activité de l'entreprise")
    logo = models.ImageField(
        upload_to=company_logo_path, 
        null=True, 
        blank=True, 
        verbose_name="Logo de l'entreprise"
    )
    is_approved = models.BooleanField(default=False, help_text="L'administrateur a-t-il approuvé cette entreprise ?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"

    def __str__(self):
        return self.name

OFFER_TYPE_CHOICES = [
    ('stage', 'Stage'),
    ('emploi', 'Emploi (CDD, CDI...)'),
    ('alternance', 'Alternance'),
    ('full_time', 'Temps plein'),
    ('part_time', 'Temps partiel'),
]

class JobOffer(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='job_offers',
        verbose_name="Entreprise"
    )
    title = models.CharField(max_length=255, verbose_name="Titre du poste")
    description = models.TextField(verbose_name="Description du poste")
    offer_type = models.CharField(
        max_length=20, 
        choices=OFFER_TYPE_CHOICES, 
        default='emploi',
        verbose_name="Type de contrat"
    )
    location = models.CharField(max_length=150, blank=True, verbose_name="Lieu")
    required_skills = models.ManyToManyField(
        'profiles.Skill', # Utilisation de la chaîne pour éviter l'import circulaire
        blank=True,
        verbose_name="Compétences requises"
    )
    is_active = models.BooleanField(default=True, verbose_name="Offre active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"

# --- CLASSE APPLICATION PLACÉE APRÈS JOBBOffer ---
class Application(models.Model):
    """
    Modèle pour représenter la candidature d'un étudiant (Profile) à une offre (JobOffer).
    """
    job_offer = models.ForeignKey(
        JobOffer, # Maintenant, JobOffer est défini au-dessus, donc Python le connaît
        on_delete=models.CASCADE, 
        related_name='applications', 
        verbose_name="Offre d'emploi"
    )
    student = models.ForeignKey(
        'profiles.Profile', # On garde la chaîne pour éviter l'import circulaire
        on_delete=models.CASCADE, 
        related_name='applications', 
        verbose_name="Candidat"
    )
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de candidature")
    cover_letter = models.TextField("Lettre de motivation", blank=True, null=True)

    class Meta:
        unique_together = ('job_offer', 'student')
        ordering = ['-applied_at']
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

    def __str__(self):
        # Utilisation de try-except pour plus de robustesse si un profil est incomplet
        try:
            student_name = self.student.user.username
        except AttributeError:
            student_name = "[Utilisateur supprimé]"
        return f"Candidature de {student_name} pour {self.job_offer.title}"
