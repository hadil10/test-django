from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

USER_TYPE_CHOICES = (
    ('student', 'Étudiant'),
    ('company', 'Entreprise'),
)
class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect, 
        required=True,
        label="Type d'utilisateur"
        )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'user_type')
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')
