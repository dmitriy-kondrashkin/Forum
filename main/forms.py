from django import forms
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _


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
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'text goes here!', 
        'rows':4, 'cols':50
        }))

    class Meta:
        model = Comment
        fields = ['content']
                 