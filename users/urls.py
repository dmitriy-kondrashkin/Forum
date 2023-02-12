from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('sign-up/', views.custom_signup, name='sign-up'),
    path('profile/<username>', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', views.user_activate, name='activate'),
    path('password_reset/', views.profile_password_reset_request, name='profile-password-reset-request'),
    path('password_reset/<uidb64>/<token>', views.profile_password_reset, name='profile-password-reset-form'),
    path('password_recovery/', views.non_auth_password_reset_request, name='non-auth-password-reset-request'),
]
