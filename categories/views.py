from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.decorators import login_required, user_passes_test\

# Create your views here.

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        category_form = forms.CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save(commit=True)
            return redirect('add_category')
    else:
        category_form = forms.CategoryForm()
    return render(request, 'add_category.html', {'form': category_form})