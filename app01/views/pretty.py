from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import PrettyModelForm, PrettyEditModelForm
from app01.utils.pagination import PagInation

# 靓号管理
def pretty_list(request):
    """查找""""""列表展示"""

    #查找指定号码
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["moblie__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = PagInation(request, queryset)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string
    }

    return render(request, "pretty_list.html", context)


def pretty_add(request):

    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')

    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):

    if request.method == "GET":
        row_object = models.PrettyNum.objects.filter(id=nid).first()
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    else:
        return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):

    models.PrettyNum.objects.filter(id=nid).delete()

    return redirect('/pretty/list')
