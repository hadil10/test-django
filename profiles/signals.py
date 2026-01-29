# profiles/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

# Le décorateur @receiver écoute les signaux.
# Ici, il écoute le signal 'post_save' envoyé par le modèle User.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crée un profil automatiquement chaque fois qu'un nouvel utilisateur est créé.
    """
    # 'created' est un booléen. Il est True si un nouvel enregistrement a été créé.
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Sauvegarde le profil chaque fois que l'objet User est sauvegardé.
    """
    # On utilise hasattr() pour vérifier si l'attribut 'profile' existe
    # avant d'essayer de le sauvegarder.
    if hasattr(instance, 'profile'):
        instance.profile.save()