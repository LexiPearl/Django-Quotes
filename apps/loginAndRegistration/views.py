from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime
from django.core.urlresolvers import reverse
from .models import User
import bcrypt

def index(request):
    print User.objects.all()
    if not 'errors' in request.session:
        request.session['errors']=[]
    return render(request, 'loginAndRegistration/index.html')

def register(request):
    today=datetime.now()
    birthday=datetime.strptime(request.POST['birthday'], '%Y-%m-%d')
    postData= {
        "name":request.POST['name'],
        "alias":request.POST['alias'],
        "email": request.POST['email'],
        "password": request.POST['password'],
        "password_confirmation":request.POST['password_confirmation'],
        "birthday": birthday,
        "today":today,
    }
    results= User.objects.UserValidator(postData)
    if results[0]:
        for err in results[1]:
            messages.error(request,err)
        return render (request, 'loginAndRegistration/index.html')
    else:
        request.session['user_id']= results[1].id
        request.session['alias']=results[1].alias
        request.session['name']=results[1].name
        return redirect(reverse('beltThreeApp:dashboard'))

def login(request):
    postData={
        "email": request.POST['email'],
        "password": request.POST['password']
    }
    results = User.objects.userLogin(postData)
    if results == None:
        messages.error(request, "wrong credentials")
        return redirect(reverse('loginAndRegistration:index'))
    elif results[0]:
        request.session['name']= results[1].name
        request.session['alias']=results[1].alias
        request.session['user_id']= results[1].id
        return redirect(reverse("beltThreeApp:dashboard"))
    else:
        messages.error(request, results[1])
        return redirect(reverse('loginAndRegistration:index'))
