from django import forms
from .models import Job, JobApplication


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'description', 'requirements',
            'responsibilities', 'job_type', 'experience_level',
            'location', 'salary_min', 'salary_max', 'salary_currency',
            'deadline', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 5}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5,
                'placeholder': 'Tell the employer why you are the best fit...'}),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status']