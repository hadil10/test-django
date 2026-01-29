from django import forms
from user.models import CustomUser
from .models import Company
from profiles.models import Job



class CompanyUserForm(forms.ModelForm):
    """
    Formulaire pour les informations de l'utilisateur (la personne de contact).
    """
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return confirm_password

class CompanyProfileForm(forms.ModelForm):
    """
    Formulaire pour les informations du profil de l'entreprise.
    """
    class Meta:
        model = Company
        fields = ['name', 'website', 'description']
        # On exclut 'user', 'is_approved' et 'logo' qui seront gérés automatiquement.
class JobForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une fiche de poste.
    """
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'salary_min', 'salary_max',
            'required_skills', 'relevant_interests'
        ]
        # On exclut 'company' qui sera ajouté automatiquement depuis la vue.
        
        widgets = {
            'required_skills': forms.CheckboxSelectMultiple,
            'relevant_interests': forms.CheckboxSelectMultiple,
        }