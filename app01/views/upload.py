import os
from django.conf import settings
from django.shortcuts import render, HttpResponse
from app01 import models
from app01.utils.form import UpForm,UpModelForm
from django.conf import settings

def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')

    file_object = request.FILES.get("avatar")

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse("...")


def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'change_file.html', {'form': form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        image_object = form.cleaned_data.get('img')


        media_path = os.path.join("media", image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data['age'],
            img = media_path
        )
        return HttpResponse("上传成功")

    return render(request, 'change_file.html', {'form': form, "title": title})


def upload_modal_form(request):
    title = "ModelForm上传"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'change_file.html', {'form': form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("上传成功")

    return render(request, 'change_file.html', {'form': form, "title": title})
