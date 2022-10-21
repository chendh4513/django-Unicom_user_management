from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import BossUpForm
import os


def boss_list(request):
    queryset = models.Boss.objects.all()
    return render(request, 'boss_list.html', {'queryset': queryset})



def boss_add(request):
    title = "新建Boss信息"
    if request.method == "GET":
        form = BossUpForm()
        return render(request, 'change_file.html', {'form': form, "title": title})

    form = BossUpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        image_object = form.cleaned_data.get('img')

        media_path = os.path.join("media", "boss", image_object.name)
        db_path = os.path.join("boss", image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data['age'],
            img=db_path
        )
        return redirect('/boss/list')

    return render(request, 'change_file.html', {'form': form, "title": title})
