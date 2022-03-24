import json

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponse, Http404
from django.http import JsonResponse
from datetime import date, datetime

from app.models import UserInfo
from app.models import ElectricIndustry
from app.models import ElectricTotal
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


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def index(Request):
    return render(Request, 'index.html', )


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
    return render(Request, 'functions/mul_source.html', {
        'path': 'mul_source'
    })


def eco_evolution(Request):
    return render(Request, 'functions/eco_evolution.html', {
        'path': 'eco_evolution'
    })


def dpm_warning(Request):
    return render(Request, 'functions/dpm_warning.html', {
        'path': 'dpm_warning'
    })


def lod_warning(Request):
    sql = 'select * from electric_industry'
    res = ElectricIndustry.objects.raw(sql)
    arr = []
    for i in res:
        arr.append(i.year)
    return render(Request, 'functions/lod_warning.html', {'years': arr, 'category': ['全社会用电总量', '农、林、牧、渔业', '工业', '建筑业',
                                                                                     '交通运输业、仓储邮政业', '信息传输、计算机服务好软件业',
                                                                                     '商业、住宿餐饮业', '金融、房地产、商务及居民服务业',
                                                                                     '公共事业及管理组织'], 'path': 'lod_warning'
                                                          })


def res_analysis(Request):
    return render(Request, 'functions/res_analysis.html', {'path': 'res_analysis'})


def edata_year(Request):
    sql = 'select * from electric_industry'
    res = ElectricIndustry.objects.raw(sql)
    arr = []
    for i in res:
        year = i.year
        content = {year: {'农、林、牧、渔业': i.agr, '工业': i.industry, '建筑业': i.construction, '交通运输业、仓储邮政业': i.trans,
                          '信息传输、计算机服务好软件业': i.infor, '商业、住宿餐饮业': i.comme, '金融、房地产、商务及居民服务业': i.financial,
                          '公共事业及管理组织': i.public}}
        arr.append(content)
    print(json.dumps(arr, ensure_ascii=False))
    return HttpResponse(json.dumps(arr, ensure_ascii=False))


def edata_predict(Request):
    sql = 'select * from electric_total'
    res = ElectricTotal.objects.raw(sql)
    arr = []
    for i in res:
        content = {'date': i.date, 'value1': i.total, 'value2': i.predict, 'previousDate': i.prevDate}
        arr.append(content)
    print(json.dumps(arr, ensure_ascii=False, cls=ComplexEncoder))
    return HttpResponse(json.dumps(arr, ensure_ascii=False, cls=ComplexEncoder))


def edata_every(Request):
    year = Request.GET.get('year')
    res = ElectricIndustry.objects.filter(year=year)
    arr = []
    for i in res:
        year = i.year
        content = {year: {'农、林、牧、渔业': i.agr, '工业': i.industry, '建筑业': i.construction, '交通运输业、仓储邮政业': i.trans,
                          '信息传输、计算机服务好软件业': i.infor, '商业、住宿餐饮业': i.comme, '金融、房地产、商务及居民服务业': i.financial,
                          '公共事业及管理组织': i.public}}
        arr.append(content)
    print(json.dumps(arr[0][year], ensure_ascii=False))
    return HttpResponse(json.dumps(arr[0][year], ensure_ascii=False))


def edata_category(Request):
    return HttpResponse(
        json.dumps(
            ['农、林、牧、渔业', '工业', '建筑业', '交通运输业、仓储邮政业', '信息传输、计算机服务好软件业', '商业、住宿餐饮业', '金融、房地产、商务及居民服务业', '公共事业及管理组织'],
            ensure_ascii=False))
