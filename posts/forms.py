from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'category': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Select categories...',
                'multiple': 'multiple'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and body.strip() == '':
            raise forms.ValidationError("Comment cannot be empty or contain only spaces.")
        return body

