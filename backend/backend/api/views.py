from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view,permission_classes
from .forms import StudentRegisterForm
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Student
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Course







from django.db.models import Q

from .forms import CourseForm

from .models import Enrollment
from .serializers import CourseSerializer
from rest_framework import status
from .forms import EnrollmentForm




from django.views.decorators.cache import never_cache


from django.contrib.auth.views import LoginView
from django.views.decorators.cache import cache_control

class CustomLoginView(LoginView):
    template_name = "login.html"
# frontend/api/views.py
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)

    if user is not None:
        return Response({"message": "Login Successful"})
    else:
        return Response({"error": "Invalid Credentials"}, status=400)




# admin add student in backend

def add_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('admin_home')   # redirect after save

    else:
        form = StudentRegisterForm()

    return render(request, 'add_students.html', {'form': form})
# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def student_login(request):

    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None:
        return Response({'error': 'Provide email and password'}, status=400)

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    user = authenticate(username=user_obj.username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'}, status=404)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_f(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)





# class MyAdminSite(AdminSite):
#     site_header = "Course Admin"

#     def login(self, request, extra_context=None):
#         response = super().login(request, extra_context)

#         if request.user.is_authenticated:
#             return HttpResponseRedirect("/home/")   #  Redirect here

#         return response    





def admin_login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                return redirect("admin_home")

            else:
                return render(request, "admin_login.html", {"error": "Invalid admin credentials"})

        except User.DoesNotExist:
            return render(request, "admin_login.html", {"error": "User not found"})

    return render(request, "admin_login.html")




@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
@staff_member_required(login_url='/')
def admin_home(request):
    query = request.GET.get('q')   # get search text

    students = Student.objects.select_related('user').all()

    if query:
        students = students.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query)
        )

    courses = Course.objects.all()

    context = {
        "students": students,
        "student_count": students.count(),
        "course_count": courses.count(),
        "query": query,
    }

    return render(request, "admin_home.html", context)


def logout_view(request):
    logout(request)
    return redirect("admin_login")    



# admin side add course
# @staff_member_required
# def add_course(request):
#     """
#     Allows admin (is_staff=True) to add a new course with:
#     - Title
#     - Description
#     - Optional YouTube video URL
#     """
#     if request.method == "POST":
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         video_url = request.POST.get("video_url", "")  # Optional, default empty

#         # Create new course
#         Course.objects.create(
#             title=title,
#             description=description,
#             video_url=video_url
#         )

#         # Redirect to course list page
#         return redirect("course_list")

#     return render(request, "add_courses.html")



# -----------------------------
# Edit Course
# -----------------------------
@never_cache
@staff_member_required(login_url='admin_login')
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'add_courses.html', {'form': form})  



@never_cache
@staff_member_required(login_url='admin_login')
def manage_courses(request):
    """
    Shows all courses with options to add, edit, delete.
    """
    courses = Course.objects.all()
    return render(request, "manage_courses.html", {"courses": courses})

@never_cache
@staff_member_required(login_url='admin_login')
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('course_list')

@never_cache
@staff_member_required(login_url='admin_login')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.user.delete()   # deletes user + student
    return redirect('admin_home')
@never_cache
@staff_member_required(login_url='admin_login')
def toggle_student_status(request, id):
    student = get_object_or_404(Student, id=id)
    user = student.user

    user.is_active = not user.is_active
    user.save()

    return redirect('admin_home')    


# from django.shortcuts import render, redirect

@never_cache
@staff_member_required(login_url='admin_login')
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CourseForm()

    return render(request, 'add_courses.html', {'form': form})  
@never_cache
@staff_member_required(login_url='admin_login')
def course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'course_list.html', {'courses': courses})    



@never_cache
@staff_member_required(login_url='admin_login')
def allocate_course(request, student_id):

    # Get selected student
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():

            enrollment = form.save(commit=False)

            # 🔥 Assign this student automatically
            enrollment.student = student

            enrollment.save()

            return redirect('allocate_course', student_id=student_id)  # Redirect back to same page to add more courses

    else:
        form = EnrollmentForm()

    return render(request, 'allocate_course.html', {
        'form': form,
        'student': student
    }) 


# @staff_member_required
# def assigned_courses_list(request):

#     enrollments = Enrollment.objects.select_related('student', 'course')
#     return render(request, 'assigned_courses_list.html', {
#         'enrollments': enrollments
#     })      



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_courses(request):
    student = request.user.student
    courses = Course.objects.filter(enrollment__student=student)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)    





@never_cache
@login_required
@staff_member_required
def delete_enrollment(request, id):
    enrollment = get_object_or_404(Enrollment, id=id)
    enrollment.delete()
    return redirect('assigned_courses_list')   # your list page name    


@never_cache
@login_required
@staff_member_required
def assigned_courses_list(request):

    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(
            user__username__icontains=query
        )
    else:
        students = Student.objects.all()

    return render(request, 'assigned_courses_list.html', {
        'students': students,
        'query': query
    })   


@never_cache
@login_required
@staff_member_required
def assign_course(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            return redirect('assigned_courses')

    else:
        form = EnrollmentForm()

    return render(request, 'assign_course.html', {
        'form': form,
        'student': student
    })