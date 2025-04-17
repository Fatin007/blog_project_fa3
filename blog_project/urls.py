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
]

# Serve media files in both development and production
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
