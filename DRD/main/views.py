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
import logging
from .forms import ImageUploadForm
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

# Set up logging
logger = logging.getLogger(__name__)

def is_not_staff(user):
    return not user.is_staff

@login_required
@user_passes_test(is_not_staff, login_url='main:login')
def home(request):
    form = ImageUploadForm()
    username = request.user.username
    user = User.objects.get(username=username)
    context = {'username': username, 'form': form, 'diagnosis_record': user.diagnosis_record}

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                context['check_flag'] = True
                image_name = default_storage.save(image_file.name, image_file)
                image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                
                try:
                    value, classes = main(image_path)
                    context['value'] = value
                    context['classes'] = str(classes)
                    if user.diagnosis_record:
                        context['previous_diagnosis_value'] = user.previous_diagnosis_value
                        context['previous_diagnosis_class'] = user.previous_diagnosis_class
                        context['uploaded_at'] = user.uploaded_at

                    if (timezone.now() - user.uploaded_at.replace(tzinfo=None)).days > 1:
                        user.diagnosis_record = True
                        user.previous_diagnosis_value = value
                        user.previous_diagnosis_class = str(classes)
                        user.uploaded_at = datetime.now()
                        user.save()

                except Exception as e:
                    logger.error(f"Error processing image: {e}")
                    context['error'] = "An error occurred while processing the image."

    return render(request, 'home.html', context)

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