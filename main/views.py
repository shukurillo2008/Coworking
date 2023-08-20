from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from . import models
from django.utils import timezone
from decimal import Decimal 
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import xlrd
import openpyxl

@login_required(login_url='login_url')
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
        'workers':worker,
        'price':models.TimePrice.objects.last()
    }

    return render(request, 'dashboard.html', context)


def student_list(request):
    search_student = request.GET.get('search')
    students = models.Student.objects
    if search_student:
            if search_student.isdigit():
                students = students.filter(origin_id=search_student)
            else:
                students = students.filter(Q(first_name__icontains=search_student) | Q(last_name__icontains=search_student)).order_by('-degree')        
    else:
        students = students.all().order_by('-degree')
    items_per_page = 10 
    paginator = Paginator(students, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
    }
    return render(request, 'student_list.html', context)


@login_required(login_url='login_url')
def create_student(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            origin_id = request.POST['origin_id']

            # qr_image = qrcode.make(origin_id)
            # image_buffer = io.BytesIO()
            # qr_image.save(image_buffer, format='PNG')

            student = models.Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                origin_id=origin_id
            )

            # student.qr_code.save(f'qr_{origin_id}.png', ContentFile(image_buffer.getvalue()), save=True)
            messages.success(request, 'Created successfully!')
        except: 
            messages.warning(request, 'This ID is Used or Some thing went wrong =(')
        return redirect('students_url')
    else:
        return render(request, 'students_create.html')


@login_required(login_url='login_url')
def create_student_by_file(request):
    file = request.FILES.get("file")
    f = models.Files.objects.create(file=file)
    
    if f.file.name.endswith('xls'):
        book = xlrd.open_workbook(file_contents=f.file.read())
        sh = book.sheet_by_index(0)

        for row_num in range(1, sh.nrows):

            row = sh.row_values(row_num)
            origin_id = row[0]
            first_name = row[1]
            last_name = row[2]
            degree = row[3]
            
            try:
                student = models.Student.objects.get(origin_id=origin_id)
                student.first_name = first_name
                student.last_name = last_name
                if degree:
                    student.degree = degree
                student.save()
            except:
                if origin_id and first_name and last_name:
                    models.Student.objects.create(first_name = first_name, last_name = last_name, origin_id = origin_id, degree = degree)
        messages.success(request, 'done')

    elif f.file.name.endswith('.xlsx'):
        book = openpyxl.load_workbook(f.file)
        sh = list(book.worksheets[0].iter_rows(values_only=True))
        
        for up, row in enumerate(sh):
            if up == 0:
                continue
            
            origin_id = row[0]
            
            if isinstance(origin_id, int):
                try:
                    student = models.Student.objects.get(origin_id=origin_id)
                    student.first_name = row[1]
                    student.last_name = row[2]
                    if row[3] is not None: 
                        student.degree = row[3]
                    student.save()
                except:
                    if row[3] is not None and row[1] is not None and row[2] is not None:
                        models.Student.objects.create(first_name=row[1], last_name=row[2], origin_id=origin_id, degree=row[3])

        messages.success(request, 'done')
    else:
        messages.error(request, 'file format must be xlsx or xls')
                        
    return redirect("students_url")


@login_required(login_url='login_url')
def student_table_make(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
    students = models.Student.objects.all().order_by('id')
    wb = openpyxl.Workbook()
    ws = wb.active

    columns = ['Origin ID', 'First Name', 'Last Name', 'Degree']
    ws.append(columns)

    for student in students:
        row = [student.origin_id, student.first_name, student.last_name, str(student.degree)]
        ws.append(row)

    wb.save(response)
    return response


@login_required(login_url='login_url')
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
        used_degree = models.UsedDegree.objects.filter(student=student).order_by('-id')

        page_number = request.GET.get('page', 1)
        items_per_page = 10  
        paginator = Paginator(used_degree, items_per_page)
        page_obj = paginator.get_page(page_number)

        context = {
            'student': student,
            'degree': page_obj,
        }

    return render(request, 'student_detail.html', context)


@login_required(login_url='login_url')
def student_delete(request):
    origin_id = request.POST.get('origin_id')
    student = models.Student.objects.get(origin_id=origin_id)
    student.delete()
    messages.success(request, 'Deleted successfully')

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


@login_required(login_url='login_url')
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


@login_required(login_url='login_url')
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


@login_required(login_url='login_url')
def worker_delete(request):
    worker_id = request.POST.get('worker_id')
    User.objects.get(id=worker_id).delete()
    messages.success(request, 'Deleted successfully')
    return redirect('index_url')


@login_required(login_url='login_url')
def change_price(request):
    try:
        price = request.POST.get('price')
        price_time = models.TimePrice.objects.last()
        price_time.price = price
        price_time.save()
        messages.success(request, 'Saved successfully!')
        return redirect('index_url')
    except:
        messages.warning(request, 'some thing went wrong')
        return redirect('index_url')
    

@login_required(login_url='login_url')
def add_degree(request):
    try:
        degree = Decimal(request.POST.get('degree'))
        student_id = int(request.POST.get('origin_id'))

        student = models.Student.objects.get(origin_id=student_id)
        old_degree = student.degree
        new_degree = old_degree + degree

        added_degree = models.AddedDegree.objects.create( 
            student=student,
            before_degree=old_degree,
            added_degree=degree, 
            after_degree=new_degree
        )

        student.degree = new_degree
        student.save()
        messages.success(request, 'Added successfully!')
    except:
        messages.warning(request, 'NOt added, some thing went wrong =(') 
    return redirect('student_edit_url',student_id)


def change_components(request):
    worker = User.objects.filter(is_superuser=False)
    company = models.CompanyComponent.objects.last()
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        about = request.POST.get('about')
        logo = request.FILES.get('logo')
        company.company_name = company_name
        company.about = about            
        if logo :
            company.logo = logo
        company.save()

    context = {
        'workers':worker,
        'price':models.TimePrice.objects.last(),
        'company':company
    }

    return render(request, 'change_components.html', context)










