from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('sign-up/', views.custom_signup, name='sign-up'),
    path('profile/<username>', views.profile, name='profile')
]
