from django import forms
from .models import Company, JobOffer

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website', 'industry', 'logo']
        labels = {
            'name': "Nom de l'entreprise",
            'description': "Description de votre entreprise",
            'website': "Site web officiel",
            'industry': "Secteur d'activité",
            'logo': "Logo de l'entreprise",
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class JobOfferForm(forms.ModelForm):
    required_skills = forms.CharField(
        label="Compétences requises (séparées par des virgules)",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Python, Gestion de projet, SEO'}),
        help_text="Entrez les compétences nécessaires, séparées par une virgule."
    )

    class Meta:
        model = JobOffer
        
        fields = [
            'title', 
            'description', 
            'offer_type', 
            'location', 
            'is_active', 
            'required_education_level'
        ]
        
        labels = {
            'title': "Titre du poste",
            'description': "Description détaillée du poste et des missions",
            'offer_type': "Type de contrat", # <-- NOM CORRECT ICI AUSSI
            'location': "Lieu (Ville, Pays)",
            'is_active': "Publier cette offre (la rendre visible aux étudiants)",
            'required_education_level': "Niveau d'études minimum requis",
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }
