from django import forms
from .models import Post
from django.contrib.auth import get_user_model


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']