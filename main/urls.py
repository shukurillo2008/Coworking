from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.studen_list, name='students_url'),
    path('student/create', views.create_student, name='student_create_url'),
    path('student/edit/<int:id>', views.student_edit, name='student_edit_url'),
    path('student/delete', views.student_delete, name='student_delete_url'),
    path('search/student/', views.search_students, name='search_url'),
    path('enterexit/', views.enter_exit, name='enter_exit_url'),
    path('error/', views.error, name='error_url'),
]