from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    path("login/", views.LoginClassView.as_view(), name="login"),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_users/delete/<int:pk>/', views.delete_user, name='delete_user'),
]