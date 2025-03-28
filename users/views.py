from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from courses.models import Enrollment
from django.contrib import messages
from .forms import CustomUserCreationForm

User = get_user_model()

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
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            # Check if user exists
            user_exists = User.objects.filter(username=username).exists()
            
            if not user_exists:
                messages.error(request, "Username does not exist.")
                return render(request, "users/login.html")
            
            # Try to authenticate
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect("courses")  # Changed to use the correct URL name
            else:
                messages.error(request, "Incorrect password.")
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug print
            messages.error(request, "An error occurred during login. Please try again.")
    
    return render(request, "users/login.html")

def register_view(request):
    """View for user registration"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("users:login")  # Redirect to login after registration
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "users/register.html", {"form": form})