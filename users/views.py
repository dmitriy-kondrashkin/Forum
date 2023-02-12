from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
"""
AUTH
"""
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
"""
IMPORT FROM CURRENT PROJECT
"""
from .forms import UserUpdateForm
from main.models import Post
# Create your views here.
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/')   
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request,f'You have been successfully\
                                 logged in as {user.username}')
                return redirect('/feed')
            else:
                for error in list(form.errors.items()):
                    messages.error(request, error)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form':form})


def custom_signup(request):
    if request.user.is_authenticated:
        return redirect('/') 
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
        else:
            for error in list(form.errors.items()):
                messages.error(request, error)
    else:
        form = SignupForm()
    return render(request, 'users/sign-up.html', {'form':form})


def custom_logout(request):
    logout(request)
    return redirect('/feed')


@login_required
def profile(request, username):
    top_posts = Post.objects.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')[:5]
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, your profile has been successfully updated!')
            return redirect('profile', user_form.username)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', {'form':form,
                                                      'top_posts':top_posts})
    return redirect('/feed')
