from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('<slug:slug>/', views.job_detail, name='job_detail'),
    path('<slug:slug>/apply/', views.apply_job, name='apply_job'),
    path('<slug:slug>/edit/', views.job_update, name='job_update'),
    path('<slug:slug>/delete/', views.job_delete, name='job_delete'),
    path('application/<int:pk>/status/', views.update_application_status, name='update_application_status'),
]