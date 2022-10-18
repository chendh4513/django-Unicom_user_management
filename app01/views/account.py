from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.form import LoginForm
from app01.utils.code import check_code
from io import BytesIO

def login(request):
    """用户登录"""

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        user_input_code = form.cleaned_data.pop("image_code")
        image_code = request.session.get("image_code", "")
        if image_code != user_input_code.upper():
            form.add_error("image_code", "验证码错误")
            return render(request, 'login.html', {"form": form})

        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form" : form})

        request.session["info"] = {"id": admin_object.id, "username" : admin_object.username}
        request.session.set_expiry(60*60*27)
        return redirect("/admin/list/")

    return render(request, 'login.html', {"form": form})


def image_code(request):
    #生成文件验证码
    img, code_string = check_code()

    request.session['image_code'] = code_string
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):

    request.session.clear()
    return redirect('/login/')