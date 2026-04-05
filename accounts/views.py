from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CompanyRegistrationForm, JobSeekerRegistrationForm
from .forms import CompanyProfileUpdateForm, JobSeekerProfileUpdateForm


def register_choice(request):
    return render(request, 'accounts/register_choice.html')


def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome! Company account created successfully.')
            return redirect('dashboard:company_dashboard')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'role': 'Company'})


def register_jobseeker(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('dashboard:user_dashboard')
    else:
        form = JobSeekerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'role': 'Job Seeker'})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:redirect_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:redirect_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_update(request):
    user = request.user
    if user.is_company():
        profile = user.company_profile
        form_class = CompanyProfileUpdateForm
    elif user.is_jobseeker():
        profile = user.seeker_profile
        form_class = JobSeekerProfileUpdateForm
    else:
        return redirect('dashboard:admin_dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard:redirect_dashboard')
    else:
        form = form_class(instance=profile)
    return render(request, 'accounts/profile_update.html', {'form': form})