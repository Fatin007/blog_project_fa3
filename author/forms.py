from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = '__all__'
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 5}),
#         }

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'id': 'required'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username', 'id': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email', 'id': 'required'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'id': 'required'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'id': 'required'}),
        }

class EditProfileForm(UserChangeForm):
    password = None 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username', 'id': 'required'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name', 'id': 'required'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'id': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email', 'id': 'required'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

        