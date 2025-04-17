from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from posts.models import Post
from . import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic import DetailView


# Create your views here.
@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save(commit=True)
            return redirect('profile')
    else:
        post_form = forms.PostForm()
    return render(request, 'add_post.html', {'form': post_form, 'type': 'Add Post'})

@method_decorator(login_required(login_url='login'), name='dispatch')
class AddPostView(CreateView):
    model = Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Add Post'
        return context

@login_required(login_url='login')
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if post.author != request.user:
        return redirect('view_post', id=id)
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save(commit=True)
            return redirect('profile')
    else:
        post_form = forms.PostForm(instance=post)
    return render(request, 'add_post.html', {'form': post_form, 'type': 'Edit Post'})

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditPostView(UpdateView):
    model = Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Edit Post'
        return context

@login_required(login_url='login')
def delete_post(request, id):
    post = Post.objects.get(id=id)
    if post.author != request.user:
        return redirect('view_post', id=id)
    post.delete()
    return redirect('profile')

def view_post(request, id):
    post = Post.objects.get(id=id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        # print("POST request received")
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            # print("Form is valid")
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # Handle parent comment for replies
            parent_id = comment_form.cleaned_data.get('parent')
            if parent_id:
                comment.parent = parent_id
                # print(f"Parent comment ID: {parent_id}")
            
            comment.save()
            # print(f"Comment saved with ID: {comment.id}")
            return redirect('view_post', id=post.id)
        # else:
            # print(f"Form errors: {comment_form.errors}")
    else:
        comment_form = forms.CommentForm()
    
    # Increment view count
    post.view_count += 1
    post.save()
    
    return render(request, 'view_post.html', {
        'post': post,
        'comment_form': comment_form
    })

class PostDetailView(DetailView):
    model = Post
    template_name = 'view_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm()
        return context
    
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.view_count += 1
        post.save()
        return post
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        
        if not request.user.is_authenticated:
            return redirect('login')
        
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            parent_id = comment_form.cleaned_data.get('parent')
            if parent_id:
                comment.parent = parent_id
            
            comment.save()
            return redirect('view_post', id=post.id)
        else:
            context = self.get_context_data(**kwargs)
            context['comment_form'] = comment_form
            return self.render_to_response(context)