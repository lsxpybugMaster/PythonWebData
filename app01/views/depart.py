from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination


def depart_list(request):
    '''展示部门列表'''
    queryset = models.Departments.objects.all()

    return render(request,'depart_list.html',{'queryset':queryset })


def depart_add(request):
    '''添加部门'''
    if request.method == 'GET':
        return render(request,'depart_add.html')
    
    title = request.POST.get('title')

    models.Departments.objects.create(title = title)

    return redirect("/depart/list/")


def depart_delete(request):
    nid = request.GET.get('nid')

    models.Departments.objects.filter(id = nid).delete()

    return redirect("/depart/list/")


def depart_edit(request,nid):

    if request.method == 'GET':
        row_object = models.Departments.objects.filter(id = nid).first()
        return render(request,'depart_edit.html',{"row_object" : row_object })
    
    title = request.POST.get('title')

    models.Departments.objects.filter(id = nid).update(title = title)

    return redirect("/depart/list/")