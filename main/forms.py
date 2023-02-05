from django import forms
from .models import Post, Comment
from django.contrib.auth import get_user_model


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control'
        }
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={
        'class':'form-control mb-3',
        }
    ))

    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Comment',
        }
    ), label='')

    class Meta:
        model = Comment
        fields = ['content']