from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post_create/', views.post_create, name='post-create'),
    path('post/<int:pk>', views.post_detail, name='post-detail'),
]