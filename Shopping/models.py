from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称')
    name = models.CharField(max_length=20, verbose_name='姓名')
    #
    gender = models.CharField(max_length=8, choices=(('male','男'), ('female', '女'), ('secrecy', '保密')), default='male')
    pay_pwd = models.CharField(max_length=128, blank=True, null=True)
    real_name = models.CharField(max_length=12, default='', verbose_name='真实姓名')
    identity_num = models.CharField(max_length=20, default='', verbose_name='身份证号')
    birthday = models.DateField(blank=True, null=True, verbose_name='出生日期')
    mobile = models.CharField(max_length=11, default='')
    # 估计是用来设置禁用用户的。
    user_status = models.BooleanField(default=True, verbose_name='用户状态')
    image = models.ImageField(default='image/default.png', upload_to='image/%Y/%m', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name




