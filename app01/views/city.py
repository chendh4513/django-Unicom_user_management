from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import CityUpModelForm


def city_list(request):
    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})



def city_add(request):
    title = "新建城市"

    if request.method == "GET":
        form = CityUpModelForm()
        return render(request, 'change_file.html', {"form": form, 'title': title})

    form = CityUpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect("/city/list/")
    return render(request, 'change_file.html', {"form": form, 'title': title})
