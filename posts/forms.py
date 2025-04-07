from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget
from cloudinary.forms import CloudinaryFileField

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    image = CloudinaryFileField(
        options={
            'folder': 'post_images/',
            'resource_type': 'auto',
            'use_filename': True,
            'unique_filename': True,
            'overwrite': True,
        },
        required=False
    )
    
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
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not isinstance(image, str):
            return image
        return None

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and body.strip() == '':
            raise forms.ValidationError("Comment cannot be empty or contain only spaces.")
        return body

