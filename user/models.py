from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Étudiant'),
        ('company', 'Entreprise'),
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='student', # Par défaut, tout nouvel utilisateur est un étudiant
        help_text="Type d'utilisateur (étudiant ou entreprise)"
    )
    pass
    
    def __str__(self):
        return self.email
