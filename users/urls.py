from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile, register_view
from education_access.views import user_logout

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('register/', register_view, name='register'),
]
