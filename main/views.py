from django.shortcuts import render,redirect
from django.contrib import messages
from . import models


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
        context = {
            'student': student
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