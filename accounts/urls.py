from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_choice, name='register_choice'),
    path('register/company/', views.register_company, name='register_company'),
    path('register/jobseeker/', views.register_jobseeker, name='register_jobseeker'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
]