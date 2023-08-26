from django.urls import path
from . import views, login_views

urlpatterns = [
    path('students/', views.student_list, name='students_url'),
    path('student/create', views.create_student, name='student_create_url'),
    path('student/edit/<int:id>', views.student_edit, name='student_edit_url'),
    path('student/delete', views.student_delete, name='student_delete_url'),
    path('', views.enter_exit, name='enter_exit_url'),
    path('error/', views.error, name='error_url'),
    path('index/', views.index, name='index_url'),
    path('price/change', views.change_price, name='change_price_url'),
    path('student/degree/add', views.add_degree, name='add_degree_url'),
    path('login/', login_views.login_views , name='login_url'),
    path('logout/', login_views.log_out, name='logout_url'),
    path("create_student_by_file/", views.create_student_by_file, name="create_student_by_file"),
    path('download/table', views.student_table_make, name='student_table_url'),
    path('change/component', views.change_components, name='change_components_url'),
    path('student/en-ex/', views.en_ex_list,  name='en_ex_list_url'),
]