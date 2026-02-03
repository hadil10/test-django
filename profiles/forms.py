from django import forms
from .models import Profile, Skill, Interest, AcademicResult


class ProfileUpdateForm(forms.ModelForm):
    """
    Formulaire pour mettre à jour le profil d'un utilisateur,
    y compris la biographie, le CV et les relations ManyToMany.
    """
    skills = forms.CharField(
        label="Mes compétences (séparées par des virgules)",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Python, Gestion de projet, Design UX'}),
        help_text="Entrez vos compétences, même si elles sont nouvelles."
    )
    
    interests = forms.CharField(
        label="Mes centres d'intérêt (séparés par des virgules)",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Intelligence Artificielle, Écologie, Jeux vidéo'}),
        help_text="Entrez vos centres d'intérêt, séparés par une virgule."
    )

    delete_cv = forms.BooleanField(
        required=False,
        label="Supprimer mon CV actuel"
    )

    class Meta:
        model = Profile
        fields = ['bio', 'cv', 'location_preference', 'education_level']
        labels = {
            'bio': "Biographie",
            'cv': "Mettre à jour mon CV",
            'location_preference': "Lieu de travail souhaité",
            'education_level': "Niveau d'études",
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.cleaned_data.get('delete_cv'):
            if profile.cv:
                profile.cv.delete(save=False) 
        
        if commit:
            profile.save()
            self.save_m2m()

        return profile

# --- FORMULAIRE : AcademicResultForm ---
class AcademicResultForm(forms.ModelForm):
    """
    Formulaire pour ajouter un résultat académique.
    """
    class Meta:
        model = AcademicResult
        fields = ['subject', 'grade', 'year']
        labels = {
            'subject': 'Matière ou Module',
            'grade': 'Note ou appréciation',
            'year': "Année d'obtention",
        }
        help_texts = {
            'grade': 'Ex: 15/20, A+, Acquis',
            'year': 'Ex: 2024',
        }
