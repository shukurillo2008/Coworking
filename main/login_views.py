from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def login_views(request):
    if request.method == 'POST':
        data_user = request.POST.get('data_user') 
        password = request.POST.get('password')
        if str(data_user).isdigit():
            user_id = User.objects.get(id = data_user)
            user = authenticate(username = user_id.username,  password=password)
        else:
            user = authenticate(username=data_user , password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'dasturga kirdingiz')
            return redirect('index_url')
        else:
            messages.error(request, 'parol yoki login hato')
        return redirect('error_url')
    return render(request, 'login.html',)


def log_out(request):
    logout(request)
    return redirect('login_url')