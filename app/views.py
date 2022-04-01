import json
import time
import os

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponse, Http404
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import date, datetime

from app.models import UserInfo
from app.models import ElectricIndustry
from app.models import ElectricTotal

from app.models import EconomyIndustry
from app.models import EconomyResource
from app.models import EconomyTotal
from app.models import Resume
import psutil

from django.contrib import auth
# from utils.json_serializable import ComplexEncoder

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# from utils.json_serializable import ComplexEncoder
from collections import Counter

from datetime import date, datetime
import json


class ComplexEncoder(json.JSONEncoder):
    """ Json 序列化数据库中的 Datetime 格式的数据，用于json.dumps """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



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
    sql = 'select * from economy_total'
    res = EconomyTotal.objects.raw(sql)
    arr = []
    for i in res:
        arr.append(i.year)
    return render(Request, 'functions/eco_evolution.html', {
        'path': 'eco_evolution',
        'years': arr
    })


def dpm_warning(Request):
    sql = 'select * from economy_industry'
    res = ElectricIndustry.objects.raw(sql)
    arr = []
    for i in res:
        arr.append(i.year)
    return render(Request, 'functions/dpm_warning.html', {
        'path': 'dpm_warning',
        'years': arr,
        'category': ['生产总值', '第一产业', '第二产业', '第三产业', '农林牧渔业', '工业', '建筑业', '批发和零售业', '交通运输业、仓储邮政业', '金融业', '房地产业', '其他']
    })

# =============================================================================================================
#                                           系统三  ： 中长期负荷预测系统

def lod_warning(Request):
    sql = 'select * from electric_industry'
    res = ElectricIndustry.objects.raw(sql)
    arr = []
    for i in res:
        arr.append(i.year)
    return render(Request,
                  'functions/lod_warning.html',
                  {'years': arr, 'category':
                      ['全社会用电总量', '农、林、牧、渔业', '工业', '建筑业',
                       '交通运输业、仓储邮政业', '信息传输、计算机服务好软件业',
                       '商业、住宿餐饮业', '金融、房地产、商务及居民服务业',
                       '公共事业及管理组织'
                       ], 'path': 'lod_warning'
                   })


def edata_year(Request):
    page = Request.GET.get('page')
    pageSize = Request.GET.get('pageSize')
    paginator = None
    sql = 'select * from electric_industry'
    res = ElectricIndustry.objects.raw(sql)
    next = True
    if page and pageSize:
        paginator = Paginator(res, pageSize)
    if paginator is not None:
        pageRes = paginator.page(int(page))
        res = pageRes.object_list
        next = pageRes.has_next()
    arr = []
    for i in res:
        year = i.year
        content = {year: {'农、林、牧、渔业': i.agr, '工业': i.industry, '建筑业': i.construction, '交通运输业、仓储邮政业': i.trans,
                          '信息传输、计算机服务好软件业': i.infor, '商业、住宿餐饮业': i.comme, '金融、房地产、商务及居民服务业': i.financial,
                          '公共事业及管理组织': i.public}}
        arr.append(content)
    # print(json.dumps({'data': arr, 'next': next}, ensure_ascii=False))
    return HttpResponse(json.dumps({'data': arr, 'next': next}, ensure_ascii=False))


def edata_predict(Request):
    sql = 'select * from electric_total'
    res = ElectricTotal.objects.raw(sql)
    arr = []
    for i in res:
        content = {'date': i.date, 'value1': i.total, 'value2': i.predict, 'previousDate': i.prevDate}
        arr.append(content)
    # print(json.dumps(arr, ensure_ascii=False, cls=ComplexEncoder))
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
    # print(json.dumps(arr[0][year], ensure_ascii=False))
    return HttpResponse(json.dumps(arr[0][year], ensure_ascii=False))


def edata_category(Request):
    return HttpResponse(
        json.dumps(
            ['农、林、牧、渔业', '工业', '建筑业', '交通运输业、仓储邮政业', '信息传输、计算机服务好软件业', '商业、住宿餐饮业', '金融、房地产、商务及居民服务业', '公共事业及管理组织'],
            ensure_ascii=False))


def cdata_year(Request):
    page = Request.GET.get('page')
    pageSize = Request.GET.get('pageSize')
    paginator = None
    sql = 'select * from economy_industry'
    res = EconomyIndustry.objects.raw(sql)
    arr = []
    next = True
    if page and pageSize:
        paginator = Paginator(res, pageSize)
    if paginator is not None:
        pageRes = paginator.page(int(page))
        res = pageRes.object_list
        next = pageRes.has_next()
    for i in res:
        year = i.year
        content = {year: {'第一产业': i.primary, '第二产业': i.secondary, '第三产业': i.tertiary, '农林牧渔业': i.animal,
                          '工业': i.indus, '建筑业': i.construction, '批发和零售业': i.wholesale,
                          '交通运输业、仓储邮政业': i.transport, '金融业': i.financial, '房地产业': i.estate, '其他': i.others,
                          '生产总值': i.total}}
        arr.append(content)
    # print(json.dumps({'data': arr, 'next': next}, ensure_ascii=False))
    return HttpResponse(json.dumps({'data': arr, 'next': next}, ensure_ascii=False))


def cdata_every(Request):
    year = Request.GET.get('year')
    res = EconomyIndustry.objects.filter(year=year)
    arr = []
    for i in res:
        year = i.year
        content = {year: {'第一产业': i.primary, '第二产业': i.secondary, '第三产业': i.tertiary, '农林牧渔业': i.animal,
                          '工业': i.indus, '建筑业': i.construction, '批发和零售业': i.wholesale,
                          '交通运输业、仓储邮政业': i.transport, '金融业': i.financial, '房地产业': i.estate, '其他': i.others}}
        arr.append(content)
    # print(json.dumps(arr[0][year], ensure_ascii=False))
    return HttpResponse(json.dumps(arr[0][year], ensure_ascii=False))


def rdata_year(Request):
    page = Request.GET.get('page')
    pageSize = Request.GET.get('pageSize')
    paginator = None
    sql = 'select * from economy_resource'
    res = EconomyResource.objects.raw(sql)
    arr = []
    next = True
    if page and pageSize:
        paginator = Paginator(res, pageSize)
    if paginator is not None:
        pageRes = paginator.page(int(page))
        res = pageRes.object_list
        next = pageRes.has_next()
    names = ['全省年末人口总数 (万人)', '人口密度 (人/平方千米)', '全省土地面积 (万平方千米)', '民族自治地方土地面积 (万平方千米)', '全省年末耕地总资源 (万公顷)', '牧草地面积 (万公顷)',
             '全省森林面积 (万公顷)', '全省森林覆盖率(%)', '全省森林蓄积量 (亿立方米)', '全省水域及水利设施用地面积 (万公顷)', '全省水能资源理论蕴藏量 (亿千瓦)',
             '全省水资源总量 (亿立方米)', '全省铁矿保有资源储量 (亿吨)', '全省煤矿保有资源储量 (亿吨)', '全省磷矿石保有资源储量 (亿吨)']
    for i in res:
        year = i.year
        content = {year: {'全省年末人口总数 (万人)': i.population, '人口密度 (人/平方千米)': i.density, '全省土地面积 (万平方千米)': i.pLandArea,
                          '民族自治地方土地面积 (万平方千米)': i.eLandArea,
                          '全省年末耕地总资源 (万公顷)': i.tLandArea, '牧草地面积 (万公顷)': i.pastureArea, '全省森林面积 (万公顷)': i.pForestArea,
                          '全省森林覆盖率(%)': i.pForestCoverage, '全省森林蓄积量 (亿立方米)': i.pForestStock,
                          '全省水域及水利设施用地面积 (万公顷)': i.pWaterArea,
                          '全省水能资源理论蕴藏量 (亿千瓦)': i.pWaterResource, '全省水资源总量 (亿立方米)': i.pWaterAmount,
                          '全省铁矿保有资源储量 (亿吨)': i.pOreResource, '全省煤矿保有资源储量 (亿吨)': i.pCoalResource,
                          '全省磷矿石保有资源储量 (亿吨)': i.pPhosphateRes}}
        arr.append(content)
    # print(json.dumps({'data': arr, 'names': names, 'next': next}, ensure_ascii=False))
    return HttpResponse(json.dumps({'data': arr, 'names': names, 'next': next}, ensure_ascii=False))


def tdata_year(Request):
    sql = 'select * from economy_total'
    res = EconomyTotal.objects.raw(sql)
    arr = [['产值', '类目', '年份']]
    names = ['工农业总产值 (亿元)', '农业总产值  (亿元)', '工业总产值(亿元)', '轻工业产值(亿元)', '重工业产值(亿元)', '农业机械总动力(万千瓦)']
    for i in res:
        year = int(i.year)
        arr.append([float(i.indusAndAgri), '工农业总产值  (亿元)', year])
        arr.append([float(i.agricultural), '农业总产值  (亿元)', year])
        arr.append([float(i.industrial), '工业总产值(亿元)', year])
        arr.append([float(i.lightIndustrial), '轻工业产值(亿元)', year])
        arr.append([float(i.HeavyIndustrial), '重工业产值(亿元)', year])
        arr.append([float(i.AgriAndMachine), '农业机械总动力(万千瓦)', year])

    # print(json.dumps({'data': arr, 'names': names}, ensure_ascii=False))
    return HttpResponse(json.dumps({'data': arr, 'names': names}, ensure_ascii=False))


def tdata_every(Request):
    year = Request.GET.get('year')
    res = EconomyTotal.objects.filter(year=year)
    arr = []
    for i in res:
        year = i.year
        content = {year: {'工农业总产值  (亿元)': i.indusAndAgri, '农业总产值  (亿元)': i.agricultural, '工业总产值(亿元)': i.industrial,
                          '轻工业产值(亿元)': i.lightIndustrial,
                          '重工业产值(亿元)': i.HeavyIndustrial, '农业机械总动力(万千瓦)': i.AgriAndMachine}}
        arr.append(content)
    # print(json.dumps(arr, ensure_ascii=False))
    return HttpResponse(json.dumps(arr[0][year], ensure_ascii=False))


def tdata_total(Request):
    sql = 'select * from economy_total'
    res = EconomyTotal.objects.raw(sql)
    arr = []
    names = ['工农业总产值 (亿元)', '农业总产值  (亿元)', '工业总产值(亿元)', '轻工业产值(亿元)', '重工业产值(亿元)', '农业机械总动力(万千瓦)']
    lists = ['第一产业', '第二产业', '第三产业']
    arr2 = []
    years = []
    for i in res:
        year = i.year
        years.append(year)
        content = {year: [float(i.indusAndAgri), float(i.agricultural), float(i.industrial), float(i.lightIndustrial),
                          float(i.HeavyIndustrial), float(i.AgriAndMachine)]}
        arr.append(content)
    sql2 = 'select * from economy_industry where year >= ' + years[0]
    res2 = ElectricIndustry.objects.raw(sql2)
    for i in res2:
        year = i.year
        content = {year: [float(i.primary), float(i.secondary), float(i.tertiary)]}
        arr2.append(content)

    return HttpResponse(
        json.dumps({'names': names, 'data': arr, 'lists': lists, 'data2': arr2, 'years': years}, ensure_ascii=False))


def tdata_all(Request):
    page = Request.GET.get('page')
    pageSize = Request.GET.get('pageSize')
    paginator = None
    sql = 'select * from economy_total'
    res = EconomyTotal.objects.raw(sql)
    content = {}
    next = True
    if page and pageSize:
        paginator = Paginator(res, pageSize)
    if paginator is not None:
        pageRes = paginator.page(int(page))
        res = pageRes.object_list
        next = pageRes.has_next()
    for i in res:
        year = i.year
        content[year] = {'工农业总产值  (亿元)': i.indusAndAgri, '农业总产值  (亿元)': i.agricultural, '工业总产值(亿元)': i.industrial,
                         '轻工业产值(亿元)': i.lightIndustrial,
                         '重工业产值(亿元)': i.HeavyIndustrial, '农业机械总动力(万千瓦)': i.AgriAndMachine}
    print(json.dumps({'data': content, 'next': next}, ensure_ascii=False))
    return HttpResponse(json.dumps({'data': content, 'next': next}, ensure_ascii=False))


@csrf_exempt
def upload(Request):
    if Request.method == "POST":
        myfile = Request.FILES.get('file', None)
        try:
            suffix = str(myfile.name.split('.')[-1])
            times = str(time.time()).split('.').pop()  # 生成时间戳，取小数点后的值
            fil = str(myfile.name.split('.')[0])
            filename = times + '_' + fil + '.' + suffix
            filename_dir = settings.MEDIA_ROOT
            print(filename_dir)
            with open(filename_dir + '\\' + filename, 'wb+') as destination:
                for chunk in myfile.chunks():
                    destination.write(chunk)
                destination.close()
        except:
            return HttpResponse(json.dumps({'msg': '上传失败', 'code': 0}))
        return HttpResponse(json.dumps({'msg': '上传成功', 'code': 1}))
    else:
        return HttpResponse(json.dumps({'msg': '上传失败', 'code': 0}))

    return HttpResponse(json.dumps({'names': names, 'data': arr, 'lists': lists, 'data2': arr2, 'years': years}, ensure_ascii=False))


# =============================================================================================================
#                                           系统四  ： 简历分析系统


def res_analysis(Request):
    """------------------------------------------
      * 访问该系统时异步加载数据可视化内容
        1. 日期行业表（左上）
        2. 年份总量表（右上）
        3. 性别数量表（下左）
        4. 主要行业数量（下中）
        5. 主要行业占比（下右）
    ------------------------------------------"""

    return render(Request, 'functions/res_analysis.html', {'path': 'res_analysis'})


def res_summary_of_date(Request):
    # for item in Resume.objects.all().values():
    #     obj_dict[item['nid']] = \
    #         {
    #             'date': item['date'],
    #             'degree': item['degree'],
    #             'location': item['location'],
    #             'industry': item['industry']
    #         }

    # 获取统计量
    each_year_sum = {}
    for item in Resume.objects.all().values().filter().order_by('date'):
        _DATE_YEAR = str(item['date'].year)
        _DATE = str(item['date'])

        try:
            each_year_sum[_DATE] += 1
        except KeyError:
            each_year_sum[_DATE] = 0

    return HttpResponse(json.dumps(each_year_sum, ensure_ascii=False, cls=ComplexEncoder))


def res_middle_bottom_bar(Request):
    # for item in Resume.objects.all().values():
    #     obj_dict[item['nid']] = \
    #         {
    #             'date': item['date'],
    #             'degree': item['degree'],
    #             'location': item['location'],
    #             'industry': item['industry']
    #         }

    # 获取统计量
    all_items = []
    for item in Resume.objects.all().values().filter().order_by('date'):
        _DATE_YEAR = str(item['date'].year)
        _DATE = str(item['date'])
        all_items.append(item['location'][:2])

    all_items_dict = dict(Counter(all_items))
    all_infos = {key: value for key, value in all_items_dict.items() if value > 1}
    all_infos_sorted = {k: v for k, v in sorted(all_infos.items(), key=lambda item: item[1], reverse=True)}

    return HttpResponse(json.dumps(all_infos_sorted, ensure_ascii=False, cls=ComplexEncoder))


def res_right_bottom_pie(Request):
    # for item in Resume.objects.all().values():
    #     obj_dict[item['nid']] = \
    #         {
    #             'date': item['date'],
    #             'degree': item['degree'],
    #             'location': item['location'],
    #             'industry': item['industry']
    #         }
    # 获取统计量

    all_items = []
    all_jobs_ind = []
    for item in Resume.objects.all().values().filter().order_by('date'):
        _DATE_YEAR = str(item['date'].year)
        _DATE = str(item['date'])
        all_items.append(item['industry'][:2])
        if item['industry'] not in all_jobs_ind:
            all_jobs_ind.append(item['industry'])
    print(all_jobs_ind)
    all_items_dict = dict(Counter(all_items))
    all_infos = {key: value for key, value in all_items_dict.items() if value > 30}
    all_infos_sorted = {k: v for k, v in sorted(all_infos.items(), key=lambda item: item[1], reverse=True)}
    return HttpResponse(json.dumps(all_infos_sorted, ensure_ascii=False, cls=ComplexEncoder))


def res_dynamic_time_series(Request):
    all_items = {}
    for item in Resume.objects.all().values().filter().order_by('date').distinct():
        _DATE_YEAR = str(item['date'].year)
        # allData中的每一年的每个领域的简历数量是多少？
        if int(_DATE_YEAR) < 2015:
            try:
                all_items[_DATE_YEAR] = all_items[_DATE_YEAR]
            except KeyError:
                all_items[_DATE_YEAR] = {}
            finally:
                from django.db import connection
                sql = f""" select count(*) from electric2022.resume where industry like '{item['industry'][:3]}%' and date like '{_DATE_YEAR}%'; """
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    dataInfo = cursor.fetchall()
                all_items[_DATE_YEAR][item['industry'][:]] = dataInfo[0][0]

    return HttpResponse(json.dumps(all_items, ensure_ascii=False, cls=ComplexEncoder))


def res_area_line(Request):
    # for item in Resume.objects.all().values():
    #     obj_dict[item['nid']] = \
    #         {
    #             'date': item['date'],
    #             'degree': item['degree'],
    #             'location': item['location'],
    #             'industry': item['industry']
    #         }

    # 获取统计量
    each_year_sum = {}
    for item in Resume.objects.all().values().filter().order_by('date'):
        _DATE_YEAR = str(item['date'].year)
        _DEGREE = item['degree']
        _DATE = str(item['date'].year)
        if _DEGREE == '本科':
            try:
                each_year_sum[_DATE] += 1
            except KeyError:
                each_year_sum[_DATE] = 0

    ret = {}
    for year_cnt in each_year_sum:
        try:
            ret[year_cnt]['year'] = int(year_cnt)
            ret[year_cnt]['value'] =  each_year_sum[year_cnt]
        except KeyError:
            ret[year_cnt] = {}
            ret[year_cnt]['year'] = int(year_cnt)
            ret[year_cnt]['value'] =  each_year_sum[year_cnt]
    return HttpResponse(json.dumps(ret, ensure_ascii=False, cls=ComplexEncoder))


# ===================================== Sys Information =============================================
def cpuInfo():
    cpuTimes = psutil.cpu_times()

    def memoryInfo(memory):
        return {
            '总内存(total)': str(round((float(memory.total) / 1024 / 1024 / 1024), 2)) + "G",
            '已使用(used)': str(round((float(memory.used) / 1024 / 1024 / 1024), 2)) + "G",
            '空闲(free)': str(round((float(memory.free) / 1024 / 1024 / 1024), 2)) + "G",
            '使用率(percent)': str(memory.percent) + '%',
            '可用(available)': (memory.available) if hasattr(memory, 'available') else '',
            '活跃(active)': (memory.active) if hasattr(memory, 'active') else '',
            '非活跃(inactive)': (memory.inactive) if hasattr(memory, 'inactive') else '',
            '内核使用(wired)': (memory.wired) if hasattr(memory, 'wired') else ''
        }

    return {
        '物理CPU个数': psutil.cpu_count(logical=False),
        '逻辑CPU个数': psutil.cpu_count(),
        'CPU使用情况': psutil.cpu_percent(percpu=True),
        '虚拟内存': memoryInfo(psutil.virtual_memory()),
        '交换内存': memoryInfo(psutil.swap_memory()),
        '系统启动到当前时刻': {
            pro: getattr(cpuTimes, pro) for pro in dir(cpuTimes) if pro[0:1] != '_' and pro not in ('index', 'count')
        },
    }


def sys_status(Request):
    computer_info = cpuInfo()
    cpu_work = round(sum(computer_info['CPU使用情况']) / psutil.cpu_count(logical=False), 2),
    loc_mem = round((float(psutil.virtual_memory().used) / 1024 / 1024 / 1024), 2)
    tot_mem = round((float(psutil.virtual_memory().total) / 1024 / 1024 / 1024), 2)
    info = {'cpu_percent': cpu_work, 'mem_percent': round(loc_mem / tot_mem, 2)}

    return HttpResponse(json.dumps(info, ensure_ascii=False, cls=ComplexEncoder))


