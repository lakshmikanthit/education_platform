from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile, register_view, login_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('register/', register_view, name='register'),
]
