from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponse, Http404
from django.http import JsonResponse
from app.models import UserInfo
from django.contrib import auth




# ---------------------------------------------------------------------------------------------------------------------
"""
@index 
Enter the entrance of the system. Then select which user to login.
Selection:
    - SuperUser  (root)
    - NormalUser (user)
    
    Password check:
        - root -> 6CH7zM
        - user -> 000000
"""
def index(Request):

    return render(Request, 'index.html',)


# ---------------------------------------------------------------------------------------------------------------------
def login(Request):
    if Request.method == 'POST':
        ret = {'status': False, 'args': ['你必须检查你的输入信息！']}
        uname = Request.POST.get('uname')
        upass = Request.POST.get('upass')
        print(uname, upass)
        matched_user = auth.authenticate(username=uname, password=upass)

        if matched_user:
            ret['status'], ret['args'] = True, []
            status = auth.login(Request, matched_user)
            return JsonResponse(ret)
        else:
            return JsonResponse(ret)

    return render(Request, 'login.html', {})


# ---------------------------------------------------------------------------------------------------------------------
def register(Request):
    if Request.method == "POST":
        ret = {'status': True, 'args': []}
        uname = Request.POST.get('uname')
        cpass = Request.POST.get('cpass')
        umarry = Request.POST.get('umarry')
        usource = Request.POST.get('usource')
        ulabel = Request.POST.get('ulabel')
        xpass = make_password(cpass, None, 'pbkdf2_sha256')
        user = UserInfo.objects.create(
            username=uname,
            password=xpass,
            marital_status=umarry,
            native_place=usource,
            national=ulabel
        )
        user.save()
        return JsonResponse(ret)
    else:
        return render(Request, 'register.html', {})



# ------------------------------------------------------------------------------
def mul_source(Request):
    return render(Request, 'functions/mul_source.html', {})


def eco_evolution(Request):
    return render(Request, 'functions/eco_evolution.html', {})


def dpm_warning(Request):
    return render(Request, 'functions/dpm_warning.html', {})


def lod_warning(Request):
    return render(Request, 'functions/lod_warning.html', {})


def res_analysis(Request):
    return render(Request, 'functions/res_analysis.html', {})

