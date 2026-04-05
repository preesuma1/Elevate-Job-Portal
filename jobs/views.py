from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job, Category, JobApplication
from .forms import JobForm, JobApplicationForm, ApplicationStatusForm
from accounts.decorators import role_required


def job_list(request):
    jobs = Job.objects.filter(status='active').select_related('company', 'category')
    categories = Category.objects.all()

    # Search & Filter
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__company_name__icontains=query)
        )
    if category_id:
        jobs = jobs.filter(category_id=category_id)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)

    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'selected_job_type': job_type,
        'location': location,
        'total_jobs': jobs.count(),
        'job_types': Job.JOB_TYPE_CHOICES,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug, status='active')
    job.views_count += 1
    job.save(update_fields=['views_count'])

    has_applied = False
    if request.user.is_authenticated and request.user.is_jobseeker():
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()

    related_jobs = Job.objects.filter(
        category=job.category, status='active'
    ).exclude(id=job.id)[:4]

    context = {
        'job': job,
        'has_applied': has_applied,
        'related_jobs': related_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
@role_required('jobseeker')
def apply_job(request, slug):
    job = get_object_or_404(Job, slug=slug, status='active')

    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', slug=slug)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard:user_dashboard')
    else:
        form = JobApplicationForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})



@login_required
@role_required('company', 'admin')
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            if request.user.is_company():
                job.company = request.user.company_profile
            elif request.user.is_admin_role() or request.user.is_superuser:
                # Admin can post on behalf — handled separately
                job.company = request.user.company_profile
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('dashboard:company_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Post New Job'})


@login_required
@role_required('company', 'admin')
def job_update(request, slug):
    job = get_object_or_404(Job, slug=slug)

    # Company can only edit their own jobs; admin can edit any
    if request.user.is_company() and job.company != request.user.company_profile:
        messages.error(request, 'You do not have permission to edit this job.')
        return redirect('dashboard:company_dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('dashboard:company_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Update Job', 'job': job})


@login_required
@role_required('company', 'admin')
def job_delete(request, slug):
    job = get_object_or_404(Job, slug=slug)

    if request.user.is_company() and job.company != request.user.company_profile:
        messages.error(request, 'You do not have permission to delete this job.')
        return redirect('dashboard:company_dashboard')

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('dashboard:company_dashboard')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
@role_required('company', 'admin')
def update_application_status(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)

    if request.user.is_company() and application.job.company != request.user.company_profile:
        messages.error(request, 'Not authorized.')
        return redirect('dashboard:company_dashboard')

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated.')
    return redirect('dashboard:company_dashboard')