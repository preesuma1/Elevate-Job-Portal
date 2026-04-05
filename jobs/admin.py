from django.contrib import admin
from .models import Job, Category, JobApplication


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'job_type', 'experience_level']
    search_fields = ['title', 'company__company_name']
    list_editable = ['status']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status']
    list_editable = ['status']