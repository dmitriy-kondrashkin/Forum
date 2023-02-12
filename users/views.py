from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.http import Http404
from django.db.models import Q, Count, BooleanField, When, Case
"""
AUTH
"""
from .forms import SignupForm, LoginForm
from django.template.loader import render_to_string, get_template
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
"""
IMPORT FROM CURRENT PROJECT
"""
from .forms import UserUpdateForm, PasswordChangeForm, PasswordResetForm
from main.models import Post
from .decorators import user_is_not_authenticated

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
            user.is_active=False
            user.save()
            email_activate(request, user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error [0] == 'This field is required.':
                    messages.error(request, 'You must pass reCAPTCHA')
                    continue                
                messages.error(request, error)
    else:
        form = SignupForm()
    return render(request, 'users/sign-up.html', {'form':form})


@login_required
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
    if user and user.is_active:
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', {'form':form,
                                                    'top_posts':top_posts})
    else:
        raise Http404
    return redirect('/feed')


def user_activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'You have passed email confirmation. Now you can log-in!')
        return redirect('login')
    else:
        messages.error(request, f'Confirmation link is invalid. Maybe it is already expired')
    return redirect('/feed')


def email_activate(request, user, to_email):
    subject = 'Forum - account activation.'
    context = {
        'user' : user.username,
        'domain' : get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : activation_token.make_token(user),
        'protocol' : 'https' if request.is_secure() else 'http',
    }
    message = get_template('users/email_activation_mail.html').render(context)
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype = 'html'
    if email.send():
        messages.success(request, f'<b>{user}</b>, to complete the registration, \
                         you need to pass <b>email confirmation.</b> \n Please, go \
                         to your <b>{to_email}</b> inbox and check it. There should \
                         be an email with instructions that we sent you!')
    else:
        messages.error(request, f'We have some problem with sending email to {email}.\
                                  Did you type it correctly?')


@login_required
def profile_password_reset_request(request):
    top_posts = Post.objects.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')[:5]
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = 'Forum - password reset.'
                data_context = {
                    'user': associated_user,
                    'domain':get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                }
                message = get_template('users/password_reset_mail.html').render(data_context)
                email = EmailMessage(subject, message, to=[associated_user.email])
                email.content_subtype = 'html'
                if email.send():
                    messages.success(request, 
                        """
                        <b>Instructions</b> have been sent \n
                        If an <b>account</b> with such an <b>email</b> exists, you will recieve it!
                        """
                    )
                else:
                    messages.error(request, 'We have problems with sending to \
                                             you a password reset email.')
            return redirect('/feed')               
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error [0] == 'This field is required.':
                messages.error(request, 'You must pass reCAPTCHA')
                continue         
            messages.error(request, error)     
    form = PasswordResetForm()
    return render(request, 'users/user_password_reset_request.html', {'form':form,
                                                              'top_posts':top_posts})


def profile_password_reset(request, uidb64, token):
    top_posts = Post.objects.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')[:5]
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        if request.method == "POST":
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your password has been set!\
                                            Now you need to log in with a new password!')
                return redirect('/login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        form = PasswordChangeForm(user)    
        return render(request, 'users/user_password_change.html', {'form':form,
                                                                   'top_posts':top_posts})
    else:
        messages.error(request, f'Confirmation link is invalid. Maybe it is already expired')
    messages.error(request, 'Something went wrong...')
    return redirect('/feed')


@user_is_not_authenticated
def non_auth_password_reset_request(request):
    top_posts = Post.objects.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')[:5]
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = 'Forum - password reset.'
                data_context = {
                    'user': associated_user,
                    'domain':get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                }
                message = get_template('users/password_reset_mail.html').render(data_context)
                email = EmailMessage(subject, message, to=[associated_user.email])
                email.content_subtype = 'html'
                if email.send():
                    messages.success(request, 
                        """
                        <b>We send you and email with instructions</b>\
                        If such an account exists, you will recieve it shortly.
                        """
                    )
                else:
                    messages.error(request, 'We have problems with sending to \
                                             you a password reset email.')
            return redirect('/feed')               
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error [0] == 'This field is required.':
                messages.error(request, 'You must pass reCAPTCHA')
                continue         
            messages.error(request, error)     
    form = PasswordResetForm()
    return render(request, 'users/non_auth_password_reset_request.html', {'form':form,
                                                                          'top_posts':top_posts})