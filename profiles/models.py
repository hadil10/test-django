# profiles/models.py

from django.db import models
from django.conf import settings
from companies.models import Company
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()  
    valid_extensions = ['.pdf', '.docx', '.doc']
    if not ext in valid_extensions:
        raise ValidationError('Extension de fichier non supportée. Les extensions autorisées sont : .pdf, .docx, .doc')
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Nom de la compétence (ex: Python, Gestion de projet)")

    def __str__(self):
        return self.name

class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Centre d'intérêt (ex: Intelligence Artificielle, Design UX)")

    def __str__(self):
        return self.name
class Formation(models.Model):
    """
    Représente un parcours de formation ou un diplôme.
    """
    title = models.CharField(max_length=200, verbose_name="Titre de la formation")
    school = models.CharField(max_length=200, verbose_name="Établissement")
    level = models.CharField(max_length=50, verbose_name="Niveau d'études", help_text="Ex: Bac+3, Master, Doctorat, Certification...")
    duration_in_years = models.PositiveSmallIntegerField(verbose_name="Durée (en années)", null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.school}"

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
class Job(models.Model):
    """
    Représente un métier ou une carrière potentielle.
    """
    title = models.CharField(max_length=200, help_text="Titre du métier (ex: Développeur Web)")
    description = models.TextField(blank=True, help_text="Description du métier, des missions, etc.")
    
    salary_min = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Fourchette basse du salaire annuel brut (ex: 35000)"
    )
    salary_max = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Fourchette haute du salaire annuel brut (ex: 55000)"
    )
    required_skills = models.ManyToManyField(
        Skill,
        related_name="jobs",
        blank=True,
        help_text="Compétences requises pour ce métier"
    )
    relevant_interests = models.ManyToManyField(
        Interest,
        related_name="jobs_by_interest", # On renomme pour éviter un conflit
        blank=True,
        help_text="Intérêts pertinents pour ce métier"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, # Si l'entreprise est supprimée, ses offres le sont aussi
        related_name='job_postings',
        help_text="L'entreprise qui publie cette fiche de poste"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    formations = models.ManyToManyField(Formation, verbose_name="Formations recommandées", blank=True)
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, help_text="Une courte biographie.")
    cv = models.FileField(upload_to='cvs/', blank=True, null=True, verbose_name="curriculum vitae (CV)", help_text="Téléchargez votre CV au format PDF." , validators=[validate_file_extension])
    skills = models.ManyToManyField(Skill, blank=True, related_name="profiles")
    interests = models.ManyToManyField(Interest, blank=True, related_name="profiles")

    def __str__(self):
        return f"Profil de {self.user.username}"

class AcademicResult(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="academic_results")
    subject = models.CharField(max_length=100, help_text="Matière (ex: Mathématiques, Histoire)")
    grade = models.CharField(max_length=10, help_text="Note ou appréciation (ex: 15/20, A+, Acquis)")
    year = models.IntegerField(help_text="Année d'obtention (ex: 2024)")

    class Meta:
        unique_together = ('profile', 'subject', 'year')

    def __str__(self):
        return f"{self.subject} ({self.year}) - {self.grade} pour {self.profile.user.username}"
    
class UserSkillEvaluation(models.Model):
    """
    Stocke l'évaluation d'une compétence par un utilisateur.
    """
    # On utilise des constantes pour rendre les choix plus lisibles
    LEVEL_CHOICES = [
        (1, 'Débutant'),
        (2, 'Initié'),
        (3, 'Intermédiaire'),
        (4, 'Avancé'),
        (5, 'Expert'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skill_evaluations')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(choices=LEVEL_CHOICES, help_text="Niveau auto-évalué de 1 à 5")

    class Meta:
        # Assure qu'un utilisateur ne peut évaluer une compétence qu'une seule fois
        unique_together = ('profile', 'skill')

    def __str__(self):
        return f"{self.profile.user.username} - {self.skill.name}: {self.get_level_display()}"


# NOUVEAU MODÈLE POUR L'ÉVALUATION DES INTÉRÊTS
class UserInterestEvaluation(models.Model):
    """
    Stocke l'évaluation d'un centre d'intérêt par un utilisateur.
    """
    INTEREST_CHOICES = [
        (1, 'Pas intéressé'),
        (2, 'Un peu intéressé'),
        (3, 'Intéressé'),
        (4, 'Très intéressé'),
        (5, 'Passionné'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='interest_evaluations')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    level = models.IntegerField(choices=INTEREST_CHOICES, help_text="Niveau d'intérêt de 1 à 5")

    class Meta:
        # Assure qu'un utilisateur ne peut évaluer un intérêt qu'une seule fois
        unique_together = ('profile', 'interest')

    def __str__(self):
        return f"{self.profile.user.username} - {self.interest.name}: {self.get_level_display()}"


