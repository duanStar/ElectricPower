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
