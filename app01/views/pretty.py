from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import *


def pretty_list(request):

    query = {}
    search_data = request.GET.get('q','')
    if search_data:
        query['mobile__contains'] = search_data
    
    queryset = models.PrettyNum.objects.filter(**query).order_by("level")

    page_obj = Pagination(request,queryset,page_size=10)

    js_form = PrettyModelForm() # js测试用

    return render(request,'pretty_list.html',{"queryset" : page_obj.page_queryset,
                                              "safestring" : page_obj.html(),
                                              "form" : js_form})                                           

  
def pretty_add(request):
    
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request,'pretty_add.html',{"form" : form})
    
    form = PrettyModelForm(data = request.POST)

    if form.is_valid():
        form.save()
        return redirect("/pretty/list")
    
    return render(request,'pretty_add.html',{"form" : form})


def pretty_delete(request,nid):
    '''删除靓号'''

    models.PrettyNum.objects.filter(id = nid).delete()

    return redirect('/pretty/list')


def pretty_edit(request,nid):
    '''编辑靓号''' 
    row_object = models.PrettyNum.objects.filter(id = nid).first()
    
    if request.method == 'GET':       
        form = PrettyEditModelForm(instance = row_object)
        return render(request,'pretty_edit.html',{"form" : form})
       
    # 更新信息row_object 到 用户POST内容
    form = PrettyEditModelForm(data = request.POST, instance = row_object)

    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    
    return render(request,'pretty_edit.html',{"form" : form})


