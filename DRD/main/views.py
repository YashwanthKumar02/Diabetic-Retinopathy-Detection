from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from datetime import date, datetime
import json
import secrets
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.core.exceptions import ValidationError
from .models import *
import os
from PIL import Image
from django.conf import settings
from .model import *
from django.core.files.storage import default_storage

# Create your views here.


def home(request):
    user = request.user
    print(user)
    context = {'user': user}

    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES['image']
        
        # Save the uploaded file to the media directory
        image_name = default_storage.save(image_file.name, image_file)
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)

        # Call the processing function
        try:
            value, classes = main(image_path)
            print(value, classes)
            context['value'] = value
            context['classes'] = classes
        except Exception as e:
            print(f"Error processing image: {e}")
            context['error'] = "An error occurred while processing the image."

        return render(request, 'home.html', context)
    
    if user.is_authenticated:
        return render(request, 'home.html', context)
    else:
        return redirect('main:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                    # If OTP is not required, log in the user directly without OTP
                    User.objects.get(username=user)
                    login(request, user)
                    return redirect('main:home')
            else:
                messages.error(request, 'Your account is not active. Please contact admin for verification.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request,"logged out Successfuly!")
    return redirect('/login')

def signup_view(request):
    if request.method == 'POST':
        try: 
            username=request.POST['username']
            first_name=request.POST['fname']
            last_name=request.POST['lname']
            user_email=request.POST['email']
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']
            
            validate_password(pass1)

            if User.objects.filter(username=username):
                messages.error(request,"Username already Exist! please try some other Username")
                return redirect('/signup')

            if User.objects.filter(email=user_email):
                messages.error(request,'Email already registered! please try some other Email ')
                return redirect('/signup')
        

            if len(username)>20:
                messages.error(request,'Username must be under 10 characters')
                return redirect('/signup')
        
            if pass1 != pass2:
                messages.error(request,"Passwords didn't match!")
                return redirect('/signup')

            if not username.isalnum():
                messages.error(request,"Username must be Alpha-Numeric!")
                return redirect('/signup')
                
            user = User.objects.create_user(username, user_email, pass1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            primary_key = user.pk
            user = authenticate(username=username, password=pass1)
            if user is not None:
                login(request, user)
                return redirect('main:home')
        except Exception and ValidationError as e:
            return render(request,'registration/signup.html',{'errors':e})

    else:

        return render(request, 'registration/signup.html')
    
    return render(request, 'registration/signup.html')