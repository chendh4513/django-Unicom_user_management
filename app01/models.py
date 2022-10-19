from django.db import models

# Create your models here.


class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")

    # user_id
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)

class Admin(models.Model):
    """管理员"""

    username = models.CharField(verbose_name="用户名", max_length=32, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="标题", max_length=32, unique=True)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")

    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

from django.core.validators import RegexValidator
class PrettyNum(models.Model):
    """靓号表"""

    moblie = models.CharField(verbose_name="手机号", max_length=11, unique=True ,validators=[RegexValidator(r'^1\d{10}$', "手机号格式错误")])
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级"),
    )

    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已使用"),
        (2, "未使用"),
    )

    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    # admin_id
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)