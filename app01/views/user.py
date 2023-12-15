from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import *

def user_list(request):
    '''用户列表'''

    queryset = models.UserInfo.objects.all()

    # for q in queryset:
    #     print(q.id, q.name,q.create_time.strftime("%Y-%m-%d"),q.get_gender_display(),
    #           q.depart.title)
    paginator = Pagination(request,queryset,2)

    return render(request,'user_list.html',{'queryset' : paginator.page_queryset,
                                            'safestring' : paginator.html()})


def user_add(request):
    '''添加用户'''
    if request.method == "GET":
        
        form = UserModelForm()

        return render(request,'user_add.html',{"form" : form})
    
    form = UserModelForm(data = request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
   
    # 如果校验失败
    return render(request,'user_add.html',{"form" : form})


def user_delete(request,nid):
    
    models.UserInfo.objects.filter(id = nid).delete()

    return redirect('/user/list/')
    
    
def user_edit(request,nid):
    '''编辑用户''' 
    row_object = models.UserInfo.objects.filter(id = nid).first()

    if request.method == 'GET':       
        form = UserModelForm(instance = row_object)
        return render(request,'user_edit.html',{"form" : form})
       
    # 更新信息row_object 到 用户POST内容
    form = UserModelForm(data = request.POST, instance = row_object)

    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    
    return render(request,'user_edit.html',{"form" : form})


