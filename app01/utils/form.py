from django import forms
from app01 import models
from django.core.validators import ValidationError
from app01.utils import encrypt , bootstrap


class UserModelForm(bootstrap.BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "gender", "create_time", "account", "depart"]


class PrettyModelForm(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ['moblie', 'price', 'level', 'status']


class PrettyEditModelForm(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ['moblie', 'price', 'level', 'status']




class AdminModelForm(bootstrap.BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "确认密码"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"}))
    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]


    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        confirm = encrypt.md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class AdminEditModelForm(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(bootstrap.BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "确认密码"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"}))

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]


    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = encrypt.md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与旧密码一致")
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        confirm = encrypt.md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class LoginForm(bootstrap.BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"}),
        required=True
    )
    password = forms.CharField(
        label="用户名",widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"})
    )

    image_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"}),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return encrypt.md5(pwd)


class TaskModelForm(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput
        }

class OrderModelForm(bootstrap.BootStrapModelForm):

    class Meta:
        model = models.Order
        exclude = ["oid", "admin"]
