"""Django imports"""
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
"""Current project imports"""
from .forms import PostCreateForm, CommentForm
from .models import Post, Vote, Comment
from users.forms import UserUpdateForm



# Create your views here.
def feed(request):
    comments = Comment.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/feed.html', {'posts':posts,
                                              'comments':comments})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.post_slug = new_post.title.lower()
            new_post.save()
            return redirect('/')
        else:
            for error in list(form.errors.items()):
                messages.error(request, error)
    else:
        form = PostCreateForm()
    return render(request,'main/post_create.html', {'form':form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(
                post = post,
                author = request.user,
                content = content
            )
            comment.save()
            return redirect(post.get_absolute_url())
        else:
            for error in list(comment_form.errors.items()):
                messages.error(request, error)
    else:
        comment_form = CommentForm()
    return render(request, 'main/post_detail.html', {'post':post,
                                                     'comment_form':comment_form,
                                                     'comments':comments})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author = request.user)
    if request.user == post.author:
        post.delete()
        return redirect('/')
    else:
        messages.error(f"It's not your post!")
    return redirect('/')


@login_required
def comment_delete(request, slug):
    comment = get_object_or_404(Comment, slug=slug, author = request.user)
    if comment.author == request.user:
        comment.delete()
        return redirect(comment.get_absolute_url())
    return redirect('/')


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostCreateForm(instance=post)
    if post.author == request.user:
        if request.method == "POST":
            form = PostCreateForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your post "{post.title}" has been successfully\
                                updated!')
                return redirect(post.get_absolute_url())
    else:
        messages.error(request, "You don't have permission to access")
        return redirect('/')
    return render(request, 'main/post_update.html', {'post':post,
                                                     'form':form})


@login_required
def comment_update(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    form = CommentForm(instance=comment)
    if comment.author == request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your comment has been successfully updated!')
                return redirect(comment.get_absolute_url())
    else:
        messages.error(request, "You don't have permission to access")
    return render(request, 'main/comment_update.html', {'form':form,
                                                        'comment':comment})


def error_404(request, exception):
    return render(request, 'static/404.html')