from datetime import date, timedelta
from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import *

class BorrowModelForm(BootstrapModelForm):
   
    class Meta:
        model = models.Borrow
        exclude = ['renewed']
        
    def __init__(self, *args, **kwargs):
        super(BorrowModelForm, self).__init__(*args, **kwargs)
        self.fields['borrow_date'].initial = date.today()
        self.fields['return_date'].initial = date.today() + timedelta(days=30)

def outdate_list(request):
    '''显示超期借阅'''
    # 查找还书时间早于当日时间的
    queryset = models.Borrow.objects.filter(return_date__lt = date.today())

    page_obj = Pagination(request,queryset,page_size=10)

    return render(request,'borrow_list.html',{"queryset" : page_obj.page_queryset,
                                              "safestring" : page_obj.html(),                                         
                                             })         

def borrow_list(request):
    '''显示借阅名单'''
    '''支持联合查询'''
    
    query = {}

    q_book = request.GET.get('book','')
    q_reader = request.GET.get('reader','')

    ## 包含外键的查询
    if q_book:
        query['book__title__contains'] = q_book
    if q_reader:
        query['reader__name__contains'] = q_reader
   
    queryset = models.Borrow.objects.filter(**query)

    page_obj = Pagination(request,queryset,page_size=10)


    # 真正分页时的数据
    q = page_obj.page_queryset

    # 获取还书时间
    # dates = list(q.values_list('return_date', flat=True))
    # 计算超期时间，没有超期则为空
    # outdates = []
    # for date in dates:
    #     if date < date.today():
    #         outdates.append( (date.today() - date).days )
    #     else:
    #         outdates.append(None)
  

    return render(request,'borrow_list.html',{"queryset" : q,
                                              "safestring" : page_obj.html(),                                         
                                             })         

def borrow_add(request):
    '''增添借阅'''
    if request.method == 'GET':
        form = BorrowModelForm()
        return render(request,'borrow_add.html',{"form" : form})
    

    form = BorrowModelForm(request.POST)


    # 判断该人是否有书不还
    have_outdate = models.Borrow.objects.filter(reader = request.POST['reader'],return_date__lt = date.today()).exists()
    
    if have_outdate:
        # 有书不还，不可借书
        return render(request,'borrow_add.html',{"form" : form , "err" : "该同学有书逾期未还,未还超期借阅前不能借阅"})

    # 查找此书对应的书行，将其库存减1
    row = models.Book.objects.get(id = request.POST['book'])
    if row.bookleft >= 1:
        row.bookleft -= 1    
        row.save()
    # 书不够了就发送错误提示
    else :
        return render(request,'borrow_add.html',{"form" : form , "err" : "该书籍已经没有馆藏,请等待其他读者归还后借阅。"})

    if form.is_valid():
        form.save()
        return redirect("/borrow/list")
    
    return render(request,'borrow_add.html',{"form" : form})


def borrow_return(request,nid,bookname):
    '''还书'''
    '''nid是借书表的编号,用于删去此借书信息'''
    '''bookname是借阅的书籍,用于还书'''
    # 查找此书对应的书行，将其库存加1
    row = models.Book.objects.get(title = bookname)
    row.bookleft += 1    
    row.save()

    models.Borrow.objects.filter(id = nid).delete()

    return redirect('/borrow/list')


def borrow_continue(request,nid):
    '''续借'''

    row = models.Borrow.objects.get(id = nid)
    row.return_date += timedelta(days=30)
    row.renewed = 1 # 取消续借权限
    row.save()

    return redirect('/borrow/list')



