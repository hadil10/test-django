from django import forms
from .models import Profile, Skill, Interest, AcademicResult

# --- FORMULAIRE : ProfileUpdateForm ---
class ProfileUpdateForm(forms.ModelForm):
    """
    Formulaire pour mettre à jour le profil d'un utilisateur,
    y compris la biographie, le CV et les relations ManyToMany.
    """
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Mes compétences"
    )
    
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Mes centres d'intérêt"
    )

    delete_cv = forms.BooleanField(
        required=False,
        label="Supprimer mon CV actuel"
    )

    class Meta:
        model = Profile
        fields = ['bio', 'cv', 'skills', 'interests']
        labels = {
            'bio': 'Ma biographie',
            'cv': 'Mon CV (format PDF, DOCX)',
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
