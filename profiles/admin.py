# profiles/admin.py

from django.contrib import admin
from .models import (
    Profile, 
    Skill, 
    Interest, 
    AcademicResult, 
    UserSkillEvaluation, 
    UserInterestEvaluation,
    Formation
)

# Méthode d'enregistrement propre avec les classes de personnalisation
# La syntaxe @admin.register(...) est un "décorateur" qui remplace admin.site.register(...)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_skills_count') # Affiche l'utilisateur et le nombre de compétences
    search_fields = ('user__username',)
    
    @admin.display(description='Nombre de compétences')
    def get_skills_count(self, obj):
        return obj.skills.count()

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AcademicResult)
class AcademicResultAdmin(admin.ModelAdmin):
    list_display = ('profile', 'subject', 'grade', 'year')
    list_filter = ('profile__user__username', 'year', 'subject') # Filtre par nom d'utilisateur
    search_fields = ('subject',)

@admin.register(UserSkillEvaluation)
class UserSkillEvaluationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'skill', 'level')
    list_filter = ('profile__user__username', 'skill__name', 'level') # Filtre par nom

@admin.register(UserInterestEvaluation)
class UserInterestEvaluationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'interest', 'level')
    list_filter = ('profile__user__username', 'interest__name', 'level') # Filtre par nom

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'level')
    search_fields = ('title', 'school')

