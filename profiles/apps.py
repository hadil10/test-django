from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
    def ready(self):
        # Importer les signaux pour créer automatiquement un profil lors de la création d'un utilisateur
        #importer les signaux pour qu'ils soient connectés au demarrage de l'application
        import profiles.signals
