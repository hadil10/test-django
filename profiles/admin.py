
from django.contrib import admin
from .models import (
    Profile, Skill, Interest, AcademicResult,
    UserSkillEvaluation, UserInterestEvaluation,
    Job, Formation
)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class AcademicResultAdmin(admin.ModelAdmin):
    list_display = ('profile', 'subject', 'grade')
    list_filter = ('profile',)

class UserSkillEvaluationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'skill', 'level')
    list_filter = ('profile', 'skill')

class UserInterestEvaluationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'interest', 'level')
    list_filter = ('profile', 'interest')

class FormationAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'level', 'duration_in_years')
    search_fields = ('title', 'school')

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'salary_min', 'salary_max', 'created_at')
    search_fields = ('title', 'description', 'company__name')
    list_filter = ('company',)
    filter_horizontal = ('required_skills', 'relevant_interests', 'formations')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(AcademicResult, AcademicResultAdmin)
admin.site.register(UserSkillEvaluation, UserSkillEvaluationAdmin)
admin.site.register(UserInterestEvaluation, UserInterestEvaluationAdmin)
admin.site.register(Formation, FormationAdmin)
admin.site.register(Job, JobAdmin)
