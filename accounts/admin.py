from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CompanyProfile, JobSeekerProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Profile', {'fields': ('role', 'phone', 'profile_picture')}),
    )


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'industry', 'is_verified']
    list_editable = ['is_verified']


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'experience_years', 'location']