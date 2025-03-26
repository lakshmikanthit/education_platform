from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from courses.models import Course, Instructor, Enrollment
from django.urls import reverse

User = get_user_model()

def is_superuser(user):
    return user.is_superuser

# Home Page View
def home(request):
    try:
        if request.user.is_authenticated:
            courses = Course.objects.all()
            instructors = Instructor.objects.all()
        else:
            # Show only limited preview for non-logged in users
            courses = Course.objects.all()[:3]  # Show only 3 courses as preview
            instructors = None
    except:
        # If there's any error with the database or models, just render the template
        courses = []
        instructors = None
    
    return render(request, 'home.html', {
        'courses': courses,
        'instructors': instructors,
    })

# List All Courses View
@login_required
def course_list(request):
    courses = Course.objects.all()
    instructors = Instructor.objects.all()
    return render(request, "education_access/courses.html", {
        "courses": courses,
        "instructors": instructors
    })

# Course Detail View
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'education_access/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "education_access/login.html")

# User Registration View
def register(request):
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
    
    return render(request, "education_access/register.html", {"form": form})

# User Logout View
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect("users:login")
    return redirect("home")

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f"Successfully enrolled in {course.title}!")
        messages.info(request, f"You can view all your enrolled courses on your <a href='{reverse('users:profile')}'>profile page</a>.")
    
    return redirect('course_detail', course_id=course_id)

@login_required
@user_passes_test(is_superuser)
def add_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        instructor_id = request.POST.get('instructor')
        duration = request.POST.get('duration')
        price = request.POST.get('price')

        try:
            instructor = Instructor.objects.get(id=instructor_id)
            course = Course.objects.create(
                title=title,
                description=description,
                instructor=instructor,
                duration=duration,
                price=price
            )
            messages.success(request, f'Course "{title}" has been added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding course: {str(e)}')
        
    return redirect('home')

@login_required
@user_passes_test(is_superuser)
def add_instructor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        try:
            instructor = Instructor.objects.create(
                name=name,
                email=email
            )
            messages.success(request, f'Instructor "{name}" has been added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding instructor: {str(e)}')
        
    return redirect('home')

@login_required
@user_passes_test(is_superuser)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.instructor_id = request.POST.get('instructor')
        course.duration = request.POST.get('duration')
        course.price = request.POST.get('price')
        
        try:
            course.save()
            messages.success(request, f'Course "{course.title}" has been updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating course: {str(e)}')
        
        return redirect('home')
    
    instructors = Instructor.objects.all()
    return render(request, 'education_access/edit_course.html', {
        'course': course,
        'instructors': instructors
    })

@login_required
@user_passes_test(is_superuser)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    try:
        course.delete()
        messages.success(request, f'Course "{course.title}" has been deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting course: {str(e)}')
    
    return redirect('home')

@login_required
def dashboard(request):
    # Get user's enrolled courses
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
    
    # Get course progress (you may need to adjust this based on your progress tracking model)
    courses_progress = []
    for enrollment in enrolled_courses:
        courses_progress.append({
            'course': enrollment.course,
            'progress': 0,  # You can calculate actual progress here
            'enrolled_date': enrollment.enrolled_date if hasattr(enrollment, 'enrolled_date') else None
        })
    
    context = {
        'enrolled_courses': enrolled_courses,
        'courses_progress': courses_progress,
        'total_courses': len(courses_progress),
        'completed_courses': 0,  # You can calculate this based on your progress tracking
    }
    
    return render(request, 'dashboard.html', context)  
