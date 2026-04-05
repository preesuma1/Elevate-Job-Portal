from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CompanyProfile, JobSeekerProfile


class CompanyRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=200)
    industry = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=200, required=False)
    website = forms.URLField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'company'
        if commit:
            user.save()
            CompanyProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                industry=self.cleaned_data.get('industry', ''),
                location=self.cleaned_data.get('location', ''),
                website=self.cleaned_data.get('website', ''),
            )
        return user


class JobSeekerRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=200)
    location = forms.CharField(max_length=200, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'jobseeker'
        if commit:
            user.save()
            JobSeekerProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                location=self.cleaned_data.get('location', ''),
            )
        return user


class CompanyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'company_logo', 'website', 'description',
                  'industry', 'location', 'established_year']


class JobSeekerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['full_name', 'resume', 'skills', 'experience_years',
                  'education', 'location', 'bio']