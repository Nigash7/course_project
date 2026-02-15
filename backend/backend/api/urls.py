from django.urls import path
from .views import login_view
# from .views import add_student
from .views import student_login
from .views import logout
from .views import admin_login
from .views import admin_home
from .views import logout_view
from .views import add_course
from .views import edit_course
from .views import manage_courses
from .views import delete_course
from . import views


urlpatterns = [
    path('login/', login_view),
    path("api/student_login/", student_login),
    path('add/student/', views.add_student, name='add_student'),
    
    path('', admin_login,name='admin_login'),
    path('api/logout/', logout, name='logout'),
    path('home/', admin_home, name='admin_home'),
    path('admin-logout/', logout_view, name="admin_logout"),
    #  path("courses/", manage_courses, name="course_list"),
    # path("courses/add/", add_course, name="add_course"),
    path('add-courses/', views.add_course, name='add_courses'),
    # path("courses/edit/<int:course_id>/", edit_course, name="edit_course"),
    path("courses/delete/<int:course_id>/", delete_course, name="delete_course"),
    path('student/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('student/toggle/<int:id>/', views.toggle_student_status, name='toggle_student_status'),

    path('courses/', views.course_list, name='course_list'),
path('course/edit/<int:id>/', views.edit_course, name='edit_course'),
path('course/delete/<int:id>/', views.delete_course, name='delete_course'),
  # path('allocate-course/', views.allocate_course, name='allocate_course'),
  path('assigned-courses/', views.assigned_courses_list, name='assigned_courses_list'),
  path('api/my-courses/', views.student_courses, name='my_courses'),
    path('delete-enrollment/<int:id>/', views.delete_enrollment, name='delete_enrollment'),
     path('allocate-course/<int:student_id>/', views.allocate_course, name='allocate_course'),


    

]