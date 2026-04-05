from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.redirect_dashboard, name='redirect_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/verify-company/<int:pk>/', views.admin_verify_company, name='admin_verify_company'),
    path('admin/delete-job/<int:pk>/', views.admin_delete_job, name='admin_delete_job'),
    path('company/', views.company_dashboard, name='company_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
]