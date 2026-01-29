from django import forms
from .models import Profile, Skill, Interest

class ProfileUpdateForm(forms.ModelForm):
    # On définit les champs pour les compétences et les intérêts
    # en utilisant un champ spécial pour les relations ManyToMany.
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple, # Affiche les choix sous forme de cases à cocher
        required=False # Le champ n'est pas obligatoire
    )
    
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    delete_cv = forms.BooleanField(
        required=False,
        label="Supprimer mon CV actuel"
    )


    class Meta:
        model = Profile
        # On liste les champs du modèle Profile que l'on veut rendre modifiables.
        fields = ['bio','cv', 'skills', 'interests']
        labels = {
            'bio': 'Ma biographie',
            'cv': 'Mon CV (format PDF, DOCX)',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}), # Affiche la bio dans une zone de texte plus grande
        }
    def save(self, commit=True):
        profile = super().save(commit=False)

        # On vérifie si la case 'delete_cv' a été cochée dans le formulaire soumis
        if self.cleaned_data.get('delete_cv'):
            # Si oui, on supprime le fichier associé au champ 'cv'
            if profile.cv:
               profile.cv.delete(save=False) 
        if commit:
            profile.save()
            # On doit aussi sauvegarder les relations ManyToMany, ce que le ModelForm fait pour nous
            self.save_m2m()

        return profile