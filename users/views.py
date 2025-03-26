from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from courses.models import Enrollment
from django.contrib import messages
from .forms import CustomUserCreationForm

# Create your views here.
@login_required
def profile(request):
    """View for user profile page"""
    # Get enrolled courses for the user
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    return render(request, 'users/profile.html', {
        'user': request.user,
        'enrollments': enrollments
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'courses')  # Default to courses if no next parameter
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "users/login.html")

def register_view(request):
    """View for user registration"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("users:login")
        else:
            messages.error(request, "Error in registration. Please check the form.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "users/register.html", {"form": form})
