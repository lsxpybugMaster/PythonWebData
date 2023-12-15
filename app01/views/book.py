from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import *

class BookModelForm(BootstrapModelForm):
   
    class Meta:
        model = models.Book
        fields = "__all__"


def book_list(request):
    '''显示图书'''
    '''支持联合查询'''
    query = {}
    q_book = request.GET.get('book','')
    q_author = request.GET.get('author','')
    q_publisher = request.GET.get("publisher",'')
    if q_book:
        query['title__contains'] = q_book
    if q_author:
        query['author__contains'] = q_author
    if q_publisher:
        query['publisher__contains'] = q_publisher
    
    queryset = models.Book.objects.filter(**query)

    page_obj = Pagination(request,queryset,page_size=10)


    return render(request,'book_list.html',{"queryset" : page_obj.page_queryset,
                                              "safestring" : page_obj.html(),
                                             })         
def book_add(request):
    '''添加图书'''
    if request.method == 'GET':
        form = BookModelForm()
        return render(request,'book_add.html',{"form" : form})
    
    form = BookModelForm(data = request.POST)

    if form.is_valid():
        form.save()
        return redirect("/book/list")
    
    return render(request,'book_add.html',{"form" : form})



def book_delete(request,nid):
    '''删除图书'''

    row = models.Book.objects.get(id = nid)
    # 判断书的馆藏和总数是否一致，一致才可以去掉此书
    if row.booktotal == row.bookleft:
        models.Book.objects.filter(id = nid).delete()
    else:
        # TODO ： 这里改为ajax处理
        queryset = models.Book.objects.filter()
        page_obj = Pagination(request,queryset,page_size=10)

        return render(request,'book_list.html',{"queryset" : page_obj.page_queryset,
                                              "safestring" : page_obj.html(),
                                              "err" : 1,
                                             })         
        


    return redirect('/book/list')


def book_edit(request,nid):
    '''修改图书''' 
    row_object = models.Book.objects.filter(id = nid).first()
    
    if request.method == 'GET':       
        form = BookModelForm(instance = row_object)
        return render(request,'book_edit.html',{"form" : form})
       
    # 更新信息row_object 到 用户POST内容
    form = BookModelForm(data = request.POST, instance = row_object)

    if form.is_valid():
        form.save()
        return redirect('/book/list/')
    
    return render(request,'book_edit.html',{"form" : form})
