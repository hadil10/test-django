from django.db import models
from django.conf import settings # Pour lier à notre CustomUser

class Company(models.Model):
    """
    Représente le profil d'une entreprise inscrite sur la plateforme.
    """
    # Le compte utilisateur qui gère cette entreprise
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='company_profile'
    )
    
    name = models.CharField(max_length=255, unique=True, help_text="Le nom officiel de l'entreprise")
    description = models.TextField(blank=True, help_text="Description de l'entreprise, sa culture, etc.")
    website = models.URLField(blank=True, help_text="Site web de l'entreprise")
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True, help_text="Logo de l'entreprise")
    
    # Statut pour la modération
    is_approved = models.BooleanField(default=False, help_text="L'administrateur a-t-il approuvé cette entreprise ?")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
