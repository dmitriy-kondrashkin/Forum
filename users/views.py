from django.shortcuts import render, redirect
"""
AUTH
"""
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form':form})


def custom_logout(request):
    logout(request)
    return redirect('/')


def custom_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/sign-up.html', {'form':form})

