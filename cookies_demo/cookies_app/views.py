from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
import requests
import django.contrib.auth
from datetime import datetime
# Utility functions to get and translate date objects, the worst kind of objects..



# Regular view functions

def home(request):
    if request.user.is_authenticated:
        dt = datetime.now()
        context= {
            'message': 'Hello World',
            'setting_cookie': False,
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'username': request.user.username,
        }
        context['setting_cookie'] = True
        return render(request, 'cookies_app/home.html', context)
    else:
        return HttpResponseRedirect(reverse('cookies_app:login'))

def login(request):
    # print(request.POST)
    # print(request.GET)
    if request.method == 'POST':
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST['g-recaptcha-response'],
            'secret': secret_key,
        }
        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        # print(result_json)
        ################################################
        if not result_json['success'] or result_json['score'] <= 0.5:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY
            }
            return render(request, 'cookies_app/login.html', context)
        ################################################
        # user login logic here
        username = request.POST['username']
        password = request.POST['password']
        user = django.contrib.auth.authenticate(
            request, username=username, password=password)
        next = request.GET.get('next', reverse('cookies_app:home'))
        return HttpResponseRedirect(next)
    context = {
        'site_key': settings.RECAPTCHA_SITE_KEY
    }
    if request.method == 'POST' and not result_json.get('success'):
        context['is_robot'] = True
    return render(request, 'cookies_app/login.html', context)

def register(request):
    # print('GET' + str(request.GET))
    if request.method == 'POST':
        django.contrib.auth.logout(request)
        # print(request.POST)
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST['g-recaptcha-response'],
            'secret': secret_key,
        }
        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        # print(result_json)
        # create user logic here
        if not result_json['success'] or result_json['score'] <= 0.5:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY
            }
            return render(request, 'cookies_app/register.html', context)
        password = request.POST['password']
        password_v = request.POST['password_v']
        if password != password_v:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY
            }
            return render(request, 'cookies_app/register.html', context)
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            user = django.contrib.auth.authenticate(
                request, username=username, password=password)
            if user is None:
                return HttpResponseRedirect(reverse('cookies_app:login'))
            django.contrib.auth.login(request, user)
            return HttpResponseRedirect(reverse('cookies_app:profile'))
        user = User.objects.create_user(
            username, request.POST['email'], password)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        django.contrib.auth.login(request, user)
        return HttpResponseRedirect(reverse('cookies_app:home'))
    context = {
        'site_key': settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, 'cookies_app/register.html', context)

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('cookies_app:login'))