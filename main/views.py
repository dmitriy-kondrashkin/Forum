"""Django imports"""
from django.shortcuts import render, redirect
"""Current project imports"""
from .forms import PostCreateForm
from .models import Post, Vote

# Create your views here.
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/feed.html', {'posts':posts})


def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('/')
    else:
        form = PostCreateForm()
    return render(request,'post_create.html', {'form':form})
