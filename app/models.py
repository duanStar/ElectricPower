# ==================================================== #


# ==================================================== #


from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """ The requirement file defined the role of All Users, we only need these fields. """
    nid = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    marital_status = models.CharField(verbose_name='婚姻状况', max_length=6)
    native_place = models.CharField(verbose_name='籍贯', max_length=32)
    national = models.CharField(verbose_name='民族', max_length=16)

    def __str__(self):
        return self.username



class ElectricIndustry(models.Model):
    year = models.CharField('年份', primary_key=True, max_length=4)
    agr = models.CharField('农、林、牧、渔业', max_length=256)
    industry = models.CharField('工业', max_length=256)
    construction = models.CharField('建筑业', max_length=256)
    trans = models.CharField('交通运输业、仓储邮政业', max_length=256)
    infor = models.CharField('信息传输、计算机服务好软件业', max_length=256)
    comme = models.CharField('商业、住宿餐饮业', max_length=256)
    financial = models.CharField('金融、房地产、商务及居民服务业', max_length=256)
    public = models.CharField('公共事业及管理组织', max_length=256)

    class Meta:
        db_table = 'electric_industry'


class ElectricTotal(models.Model):
    date = models.DateTimeField('当前日期', primary_key=True)
    total = models.CharField('全社会用电总量', max_length=256)
    predict = models.CharField('预测全社会用电总量', max_length=256)
    prevDate = models.DateTimeField('上个日期')

    class Meta:
        db_table = 'electric_total'

class Resume(models.Model):
    nid = models.AutoField(primary_key=True)
    date = models.DateField('投递日期', max_length=64)
    degree = models.CharField('学历', max_length=16)
    location = models.CharField('所在地', max_length=256)
    industry = models.CharField('行业', max_length=32)

    class Meta:
        db_table = 'resume'

class EconomyIndustry(models.Model):
    year = models.CharField('年份', primary_key=True, max_length=4)
    primary = models.CharField('第一产业', max_length=256)
    secondary = models.CharField('第二产业', max_length=256)
    tertiary = models.CharField('第三产业', max_length=256)
    animal = models.CharField('农林牧渔业', max_length=256)
    indus = models.CharField('工业', max_length=256)
    construction = models.CharField('建筑业', max_length=256)
    wholesale = models.CharField('批发和零售业', max_length=256)
    transport = models.CharField('交通运输业、仓储邮政业', max_length=256)
    financial = models.CharField('金融业', max_length=256)
    estate = models.CharField('房地产业', max_length=256)
    others = models.CharField('其他', max_length=256)
    total = models.CharField('生产总值', max_length=256)

    class Meta:
        db_table = 'economy_industry'


class EconomyResource(models.Model):
    year = models.CharField('年份', primary_key=True, max_length=4)
    population = models.CharField('全省年末人口总数 (万人)', max_length=256)
    density = models.CharField('人口密度 (人/平方千米)', max_length=256)
    pLandArea = models.CharField('全省土地面积 (万平方千米)', max_length=256)
    eLandArea = models.CharField('民族自治地方土地面积 (万平方千米)', max_length=256)
    tLandArea = models.CharField('全省年末耕地总资源 (万公顷)', max_length=256)
    pastureArea = models.CharField('牧草地面积 (万公顷)', max_length=256)
    pForestArea = models.CharField('全省森林面积 (万公顷)', max_length=256)
    pForestCoverage = models.CharField('全省森林覆盖率(%)', max_length=256)
    pForestStock = models.CharField('全省森林蓄积量 (亿立方米)', max_length=256)
    pWaterArea = models.CharField('全省水域及水利设施用地面积 (万公顷)', max_length=256)
    pWaterResource = models.CharField('全省水能资源理论蕴藏量 (亿千瓦)', max_length=256)
    pWaterAmount = models.CharField('全省水资源总量 (亿立方米)', max_length=256)
    pOreResource = models.CharField('全省铁矿保有资源储量 (亿吨)', max_length=256)
    pCoalResource = models.CharField('全省煤矿保有资源储量 (亿吨)', max_length=256)
    pPhosphateRes = models.CharField('全省磷矿石保有资源储量 (亿吨)', max_length=256)

    class Meta:
        db_table = 'economy_resource'


class EconomyTotal(models.Model):
    year = models.CharField('年份', primary_key=True, max_length=4)
    indusAndAgri = models.CharField('工农业总产值  (亿元)', max_length=256)
    agricultural = models.CharField('农业总产值  (亿元)', max_length=256)
    industrial = models.CharField('工业总产值(亿元)', max_length=256)
    lightIndustrial = models.CharField('轻工业产值(亿元)', max_length=256)
    HeavyIndustrial = models.CharField('重工业产值(亿元)', max_length=256)
    AgriAndMachine = models.CharField('农业机械总动力(万千瓦)', max_length=256)

    class Meta:
        db_table = 'economy_total'




