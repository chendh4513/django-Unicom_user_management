from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app01.utils.pagination import PagInation


# 用户管理
def admin_list(request):

    #搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["moblie__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    page_object = PagInation(request, queryset)

    context = {
        "queryset" : page_object.page_queryset,
        "page_string" : page_object.html(),
        "search_data" : search_data
    }

    return render(request, 'admin_list.html', context)

def admin_add(request):

    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, "change.html", {"form": form, "title": title})

def admin_edit(request, nid):

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    else:
        return render(request, "change.html", {"form": form, "title": title})

def admin_delete(request, nid):

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    models.Admin.objects.filter(id=nid).delete()

    return redirect('/admin/list')

def admin_reset(request, nid):

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = "重置密码-{}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"form": form, "title": title})
