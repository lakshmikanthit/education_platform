from django.shortcuts import render, redirect
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

def register_view(request):
    """View for user registration"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Error in registration. Please check the form.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "users/register.html", {"form": form})
