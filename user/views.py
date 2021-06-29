from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .forms import usersignup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from products.models import Product

def signup(request):
    print("test1")
    if request.method == 'post':
        print("test2")
        name = request.POST.get('username')
        print("test3 = ", name)
        form = usersignup(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            print("test4 = ", username)
            messages.success(request,f'Your account has been created! You can now Sign In')
            return redirect('sign_in')

    else:
        form = usersignup()
    return render(request,'signup.html',{'form':form})


