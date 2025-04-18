from django.contrib import admin
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('author/', include('author.urls')),
    path('post/', include('posts.urls')),
    path('category/', include('categories.urls')),
    path('category/<slug:slug>/', views.home, name='category_posts'),
    path('', include('home.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # Add CKEditor 5 URLs
]

# Serve media files in both development and production
# This ensures the URLs still work even though actual storage might be Cloudinary in production
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
