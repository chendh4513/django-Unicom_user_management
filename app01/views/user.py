from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UserModelForm
from app01.utils.pagination import PagInation


# 用户管理
def user_list(request):

    queryset = models.UserInfo.objects.all()

    page_object = PagInation(request, queryset)

    context = {
        "queryset" : page_object.page_queryset,
        "page_string" : page_object.html()
    }

    return render(request, 'user_list.html', context)


def user_add(request):

    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    ac = request.POST.get("ac")
    ge = request.POST.get("ge")
    de = request.POST.get("de")
    ctime = request.POST.get("ctime")

    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=ac, depart_id=de, gender=ge,
                                   create_time=ctime)
    return redirect("/user/list")


def user_model_form_add(request):

    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):

    if request.method == "GET":
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_model_form_add.html", {"form": form})


def user_delete(request, nid):

    models.UserInfo.objects.filter(id=nid).delete()

    return redirect('/user/list')
