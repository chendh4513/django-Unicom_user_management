from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import PagInation


# 部门管理
def depart_list(request):

    queryset = models.Department.objects.all()

    page_object = PagInation(request, queryset)

    context = {
        "queryset" : page_object.page_queryset,
        "page_string" : page_object.html()
    }
    return render(request, 'depart_list.html', context)

def depart_add(request):

    if request.method == 'GET':
        return render(request, 'depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)

    return redirect("/depart/list/")

def depart_delete(request):

    nid = request.GET.get('nid')

    models.Department.objects.filter(id=nid).delete()

    return redirect("/depart/list/")

def depart_edit(request, nid):

    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})
    title = request.POST.get("title")

    models.Department.objects.filter(id=nid).update(title=title)

    return redirect("/depart/list/")