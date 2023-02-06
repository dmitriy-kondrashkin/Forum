"""Django imports"""
from django.shortcuts import render, redirect, get_object_or_404
"""Current project imports"""
from .forms import PostCreateForm, CommentForm
from .models import Post, Vote, Comment
from django.contrib.auth.decorators import login_required

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
        comment_form = CommentForm()
    return render(request, 'main/post_detail.html', {'post':post,
                                                     'comment_form':comment_form,
                                                     'comments':comments})
