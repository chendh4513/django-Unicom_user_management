import json

from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.form import TaskModelForm
from app01 import models
from app01.utils.pagination import PagInation

@csrf_exempt
def task_list(request):

    queryset = models.Task.objects.all().order_by('-id')
    form = TaskModelForm()
    page_string = PagInation(request,queryset)
    context = {
        "form" : form,
        "queryset" : page_string.page_queryset,
        "page_string":page_string.html()
    }

    return render(request, "task_list.html", context)
@csrf_exempt
def task_add(request):

    form =  TaskModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        data_dict = {"status" : True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status":False, "error":form.errors}
    return HttpResponse(json.dumps(data_dict))

def task_delete(request, nid):

    models.Task.objects.filter(id=nid).delete()
    return redirect('/task/list')