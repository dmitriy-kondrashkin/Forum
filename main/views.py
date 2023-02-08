"""Django imports"""
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import JsonResponse
"""Current project imports"""
from .forms import PostCreateForm, CommentForm
from .models import Post, Comment
from users.forms import UserUpdateForm
from .utils import is_ajax
from django.db.models import Q, Count, BooleanField




# Create your views here.
def feed(request, slug):
    comments = Comment.objects.all()
    count_filter = Q(votes=request.user)
    vote_case = Count('votes', filter=count_filter, output_field=BooleanField())
    posts = Post.objects \
    .annotate(is_voted=vote_case) \
    .all().order_by('-created_at')
    return render(request, 'main/feed.html', {'posts': posts,
                                              'comments': comments})


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
    comments = Comment.objects.filter(post=post, reply=None).order_by('-created_at')
    is_voted = False
    if post.votes.filter(id=request.user.id).exists():
        is_voted = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(
                post = post,
                author = request.user,
                content = content,
                reply = comment_qs
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
                                                     'comments':comments,
                                                     'is_voted':is_voted})


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
def post_vote(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('id'), slug=slug)
    is_voted = False
    if post.votes.filter(id=request.user.id).exists():
        post.votes.remove(request.user)
        is_voted = False
    else:
        post.votes.add(request.user)
        is_voted = True
    context = {
        'post': post,
        'is_voted': is_voted,
    }
    if is_ajax(request):
        html = render_to_string('main/votes.html', context, request)
        return JsonResponse({'form':html})


@login_required
def comment_delete(request, slug):
    comment = get_object_or_404(Comment, slug=slug, author = request.user)
    if comment.author == request.user:
        comment.delete()
        return redirect(comment.get_absolute_url())
    return redirect('/')


@login_required
def reply_comment_delete(request, slug):
# get current comment, get replies for current comment, check if reply author is request user, then delete reply
    comment = get_object_or_404(Comment, slug=slug)
    reply = Comment.objects.filter(reply_id = comment.id, author = request.user).first()
    #such id reply which will equal to comment id
    if reply:
        if reply.author == request.user:
            reply.delete()
            return redirect(comment.get_absolute_url())
    else:
        messages.error(request, "You don't have permission to do that!")
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