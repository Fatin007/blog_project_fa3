from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500)
    body = RichTextField()
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image', folder='post_images/', blank=True, null=True, resource_type='auto')

    def __str__(self):
        return self.title
    
    @property
    def image_url(self):
        if self.image:
            return str(self.image)
        return None

    def save(self, *args, **kwargs):
        if self.image is None or self.image == '' or str(self.image).strip() == '':
            self.image = None
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    def __str__(self):
        return self.body
