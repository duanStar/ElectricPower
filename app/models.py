

# ==================================================== #





# ==================================================== #


from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    marital_status = models.CharField(verbose_name='婚姻状况', max_length=6)
    native_place = models.CharField(verbose_name='籍贯', max_length=32)
    national = models.CharField(verbose_name='民族', max_length=16)


    def __str__(self):
        return self.username
