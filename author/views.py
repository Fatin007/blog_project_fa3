from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = forms.RegistrationForm()
    return render(request, 'register.html', {'form': form, 'type': 'Register'})

def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('profile')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'form': form, 'type': 'Login'})

class LoginClassView(LoginView):
    template_name = 'register.html'
    form_class = AuthenticationForm
    reverse_lazy = 'profile'
    def form_valid(self, form):
        messages.success(self.request, 'Login successful.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile')


@login_required(login_url='login')
def profile(request):
    data=Post.objects.filter(author=request.user).order_by('-view_count')
    return render(request, 'profile.html', {'data': data})

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = forms.EditProfileForm(request.POST, instance=request.user)
        profile_form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        user_form = forms.EditProfileForm(instance=request.user)
        profile_form = forms.UserProfileForm(instance=request.user.profile)
    
    return render(request, 'edit_profile.html', {
        'user_form': user_form, 
        'profile_form': profile_form, 
        'type': 'Edit Profile'
    })

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password changed successfully.')
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form, 'type': 'Change Password'})

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('manage_users')

