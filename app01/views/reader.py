from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import *

class ReaderModelForm(BootstrapModelForm):
   
    class Meta:
        model = models.Reader
        fields = "__all__"


def reader_list(request):
    '''显示读者'''
    '''支持联合查询'''
    query = {}
    q_name = request.GET.get('name','')
    q_depart = request.GET.get('depart','')
    q_grade = request.GET.get('grade','')
    if q_name:
        query['name__contains'] = q_name
    if q_depart:
        query['departname__contains'] = q_depart
    if q_grade:
        query['grade__contains'] = q_grade
    
    queryset = models.Reader.objects.filter(**query)

    page_obj = Pagination(request,queryset,page_size=10)


    return render(request,'reader_list.html',{"queryset" : page_obj.page_queryset,
                                              "safestring" : page_obj.html(),
                                             })         
def reader_add(request):
    '''添加图书'''
    if request.method == 'GET':
        form = ReaderModelForm()
        return render(request,'reader_add.html',{"form" : form})
    
    form = ReaderModelForm(data = request.POST)

    if form.is_valid():
        form.save()
        return redirect("/reader/list")
    
    return render(request,'reader_add.html',{"form" : form})



def reader_delete(request,nid):
    '''删除读者'''
    # 找到要删除的读者名
    row = models.Reader.objects.get(id = nid)
    # 注意外键查询的特殊性
    hasbook = models.Borrow.objects.filter(reader__name = row.name).exists()

    # 如果读者借了书，此时不可以删除读者
    if hasbook:
        mod = models.Reader.objects.filter()
        page_obj = Pagination(request,mod,page_size=10)
        return render(request,'reader_list.html',{"queryset" : page_obj.page_queryset,
                                                  "safestring" : page_obj.html(),
                                                  "cannotdelete": 1,
                                                 })         
    else:
        models.Reader.objects.filter(id = nid).delete()
    
    return redirect('/reader/list')


def reader_edit(request,nid):
    '''修改图书''' 
    row_object = models.Reader.objects.filter(id = nid).first()
    
    if request.method == 'GET':       
        form = ReaderModelForm(instance = row_object)
        return render(request,'reader_edit.html',{"form" : form})
       
    # 更新信息row_object 到 用户POST内容
    form = ReaderModelForm(data = request.POST, instance = row_object)

    if form.is_valid():
        form.save()
        return redirect('/reader/list/')
    
    return render(request,'reader_edit.html',{"form" : form})
