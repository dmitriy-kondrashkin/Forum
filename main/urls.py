from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post_create/', views.post_create, name='post-create'),
    path('post/<slug>/', views.post_detail, name='post-detail'),
    path('post/<slug>/delete', views.post_delete, name='post-delete'),
    path('post/<slug>/update', views.post_update, name='post-update'),
    path('post/<slug>/upvote', views.post_upvote, name='post-upvote'),
    path('post/<slug>/downvote', views.post_downvote, name='post-downvote'),
    path('comment/<slug>/delete', views.comment_delete, name='comment-delete'),
    path('comment/<slug>/update', views.comment_update, name='comment-update'),
    path('comment_reply/<slug>/delete', views.reply_comment_delete, name='comment-reply-delete'),
    path('comment_reply/<slug>/update', views.reply_comment_update, name='comment-reply-update'),
]