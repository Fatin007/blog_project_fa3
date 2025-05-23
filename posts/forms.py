from django import forms
from .models import Post, Comment
from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'view_count']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'category': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Select categories...',
                'multiple': 'multiple'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'body': CKEditor5Widget(
                config_name='extends',
                attrs={'class': 'django_ckeditor_5'},
            )
        }

class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Comment
        fields = ['body', 'parent']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
        
    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and body.strip() == '':
            raise forms.ValidationError("Comment cannot be empty or contain only spaces.")
        return body
        
    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent:
            try:
                return Comment.objects.get(id=parent)
            except Comment.DoesNotExist:
                return None
        return None

