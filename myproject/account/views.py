from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib import messages
from .forms import ProfileForm, UserRegistrationForm
from .models import Profile
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView


def home(request):
    return render(request, 'account/home.html')


class password_reset_complete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


@login_required
def view_profile(request, username): 
    user = get_object_or_404(user, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'account/view_profile.html', {'profile': profile})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/home/')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('account:profile_detail')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'account/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/login/')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile_detail(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()
    return render(request, 'account/profile_detail.html', {'profile': profile})


@login_required
def profile_update(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('account:profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'account/profile_update.html', {'form': form})


@login_required
def profile_delete(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Your profile was successfully deleted!')
        return redirect('home')
    return render(request, 'account/profile_delete.html', {'profile': profile})


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('account:profile_detail')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/password_change.html', {'form': form})


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                subject_template_name='account/password_reset_subject.txt',
                email_template_name='account/password_reset_email.html',
                html_email_template_name='account/password_reset_email.html',
            )
            messages.success(
                request, 'An email has been sent with instructions to reset your password.')
            return redirect('account:password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'account/password_reset.html', {'form': form})


class password_reset_done(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class password_reset_confirm(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('account:profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'account/profile_edit.html', {'form': form})
