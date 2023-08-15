from django.shortcuts import render,redirect
from django.contrib import messages
from . import models
from datetime import datetime
from django.utils import timezone
from decimal import Decimal 
from django.contrib.auth.models import User


def index(request):
    student = models.Student.objects.all()
    visit = models.EnterExit.objects.all()
    worker = User.objects.filter(is_superuser=False)
    visits_all = 0
    visits_today = 0
    used_degree = 0
    used_degree_all = 0
    not_used_degree = 0
    students = student.count()

    for degree in models.UsedDegree.objects.all():
        used_degree_all += degree.used_degree
        if degree.created_time.day == timezone.now().day and degree.created_time.year == timezone.now().year:
            used_degree += degree.used_degree

    for degree in student:
        not_used_degree += degree.degree

    for visit in visit:
        visits_all += 1
        if visit.enter_time.day == timezone.now().day and visit.enter_time.year == timezone.now().year:
            visits_today += 1

    context = {
        'students':students,
        'visits_today':visits_today,
        'visits_all':visits_all,
        'used_degree':used_degree,
        'used_degree_all':used_degree_all,
        'not_used_degree':not_used_degree,
        'workers':worker
    }

    return render(request, 'dashboard.html', context)


def studen_list(request):
    student = models.Student.objects.all().order_by('-origin_id')
    context = {
        'students': student
    }
    return render(request, 'student_list.html', context)


def create_student(request):
    try:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        origin_id = request.POST['origin_id']

        models.Student.objects.create(
            first_name = first_name,
            last_name = last_name,
            origin_id = origin_id,
        )
        messages.success(request, 'Created successfully!')
    except: 
        messages.warning(request, 'This ID is Used or Some thing went wrong =(')
        
    return redirect('students_url')


def student_edit(request, id):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        origin_id = request.POST['origin_id']
        try:
            student = models.Student.objects.get(id=id)
            student.first_name = first_name
            student.last_name = last_name
            if int(origin_id) != id:
                student.origin_id = int(origin_id)
            student.save()
            messages.success(request , 'Changed successfully!')
        except:
            messages.warning(request, 'This ID is Used or Some thing went wrong =(')
        return redirect('student_edit_url',origin_id)
    else:
        student = models.Student.objects.get(origin_id=id)
        used_degree = models.UsedDegree.objects.filter(student = student).order_by('-id')
        context = {
            'student': student,
            'degree': used_degree
        }
    return render(request, 'student_detail.html', context)


def student_delete(request):
    origin_id = request.POST.get('origin_id')
    student = models.Student.objects.get(origin_id=origin_id)
    student.delete()
    messages.success(request, 'Deleted successfully')

    return redirect('students_url')


def search_students(request):
    search_student = request.GET.get('search')
    if search_student:
        return redirect('student_edit_url', search_student)
    else:
        return redirect('students_url')
    

def enter_exit(request):
    context = {}

    if request.method == 'POST':
        origin_id = request.POST.get('origin_id')
        
        if origin_id:
            try:
                student = models.Student.objects.get(origin_id=origin_id)
                try:
                    enterexit = models.EnterExit.objects.get(student=student, in_out=False)
                    
                    price = models.TimePrice.objects.last()
                    enterexit.in_out = True
                    enterexit.exit_time = timezone.now()
                    enterexit.save()
                    
                    time_difference = enterexit.exit_time - enterexit.enter_time
                    time_hours = time_difference.total_seconds() / 3600
                    
                    total_cost = price.price * Decimal(str(time_hours))
                    student.degree -= total_cost

                    models.UsedDegree.objects.create(
                        student = student,
                        enter_exit = enterexit,
                        before_degree = models.Student.objects.get(origin_id=origin_id).degree,
                        used_degree = total_cost,
                        after_degree = student.degree,
                    )

                    student.save()
                    
                    messages.success(request, f'Exited. Total cost: {total_cost:.2f}')
                    context['student'] = student

                except:

                    models.EnterExit.objects.create(
                        student = student,
                        enter_time = timezone.now(),
                        in_out = False,
                    )
                    messages.success(request, 'Entered')
                    context['student'] = student
            except:
                messages.error(request, 'Not Found 404')
                return redirect('error_url')
    return render(request, 'enter_exit.html', context)


def error(request):
    return render(request, 'error.html')


def worker_edit(request, id):
    if request.method == 'POST':
        worker = User.objects.get(id = id)
        worker.username = request.POST.get('username')
        worker.password = request.POST.get('password')
        worker.save()

    worker = User.objects.get(id = id)
    context = {
        'worker': worker
    }
    return render(request, 'worker_detail.html', context)


def worker_create(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = User.objects.create_user(
        username=username, 
        password=password,
        is_staff=True
        )
    messages.success(request, 'Created successfully!')
    return redirect('index_url')


def worker_delete(request):
    worker_id = request.POST.get('worker_id')
    User.objects.get(id=worker_id).delete()
    messages.success(request, 'Deleted successfully')
    return redirect('index_url')