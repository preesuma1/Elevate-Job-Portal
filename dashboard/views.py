from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from jobs.models import Job, JobApplication, Category
from accounts.models import CustomUser, CompanyProfile
from django.contrib import messages


@login_required
def redirect_dashboard(request):
    user = request.user
    if user.is_superuser or user.is_admin_role():
        return redirect('dashboard:admin_dashboard')
    elif user.is_company():
        return redirect('dashboard:company_dashboard')
    else:
        return redirect('dashboard:user_dashboard')


@login_required
@role_required('admin')
def admin_dashboard(request):
    context = {
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(status='active').count(),
        'total_users': CustomUser.objects.filter(role='jobseeker').count(),
        'total_companies': CompanyProfile.objects.count(),
        'total_applications': JobApplication.objects.count(),
        'recent_jobs': Job.objects.order_by('-created_at')[:10],
        'recent_applications': JobApplication.objects.order_by('-applied_at')[:10],
        'all_companies': CompanyProfile.objects.select_related('user').all(),
        'categories': Category.objects.all(),
        'pending_companies': CompanyProfile.objects.filter(is_verified=False),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@role_required('admin')
def admin_verify_company(request, pk):
    company = get_object_or_404(CompanyProfile, pk=pk)
    company.is_verified = not company.is_verified
    company.save()
    status = "verified" if company.is_verified else "unverified"
    messages.success(request, f'{company.company_name} has been {status}.')
    return redirect('dashboard:admin_dashboard')


@login_required
@role_required('admin')
def admin_delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted by admin.')
    return redirect('dashboard:admin_dashboard')


@login_required
@role_required('company')
def company_dashboard(request):
    company = request.user.company_profile
    jobs = Job.objects.filter(company=company).order_by('-created_at')
    applications = JobApplication.objects.filter(
        job__company=company
    ).select_related('applicant', 'job').order_by('-applied_at')

    context = {
        'company': company,
        'jobs': jobs,
        'applications': applications,
        'total_jobs': jobs.count(),
        'active_jobs': jobs.filter(status='active').count(),
        'total_applications': applications.count(),
        'pending_applications': applications.filter(status='pending').count(),
    }
    return render(request, 'dashboard/company_dashboard.html', context)


@login_required
@role_required('jobseeker')
def user_dashboard(request):
    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job', 'job__company').order_by('-applied_at')

    context = {
        'applications': applications,
        'total_applied': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'rejected': applications.filter(status='rejected').count(),
    }
    return render(request, 'dashboard/user_dashboard.html', context)