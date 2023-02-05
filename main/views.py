"""Django imports"""
from django.shortcuts import render, redirect
"""Current project imports"""
from .forms import PostCreateForm, CommentForm
from .models import Post, Vote, Comment

# Create your views here.
def feed(request):
    comments = Comment.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/feed.html', {'posts':posts,
                                              'comments':comments})


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
    return render(request,'main/post_create.html', {'form':form})


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    ied = pk
    comments = Comment.objects.filter(post=post).order_by('-pk')
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
                                                     'comments':comments,
                                                     'ied':ied})