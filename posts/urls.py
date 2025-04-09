from django.urls import path, include
from . import views

urlpatterns = [
    # path('add/', views.add_post, name='add_post'),
    path('add/', views.AddPostView.as_view(), name='add_post'),
    # path('edit/<int:id>/', views.edit_post, name='edit_post'),
    path('edit/<int:id>/', views.EditPostView.as_view(), name='edit_post'),
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
    path('view/<int:id>/', views.view_post, name='view_post'),
    # path('view/<int:id>/', views.PostDetailView.as_view(), name='view_post'),
]