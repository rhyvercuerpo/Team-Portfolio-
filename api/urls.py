from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('projects/', views.projects, name='projects'),
    path('project1/', views.project1, name='project1'),
    path('project2/', views.project2, name='project2'),
    path('project3/', views.project3, name='project3'),
    path('project4/', views.project4, name='project4'),
    path('project5/', views.project5, name='project5'),
    path('project5/api/', views.project5_api, name='project5_api'),
    path('project6/', views.project6, name='project6'),
    path('project6/api/', views.email_api, name='email_api'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('api/security-demo/', views.api_security_demo, name='api_security_demo'),
]








    # Removed duplicate allauth.urls - it's already in main urls.py
