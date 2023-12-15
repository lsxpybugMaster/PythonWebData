from django.urls import path
from app01.views import depart,pretty,user,admin,account,order,book,reader,borrow,mainpage


urlpatterns = [
    
    path('depart/list/',depart.depart_list),
    path('depart/add/' ,depart.depart_add),
    path('depart/delete/',depart.depart_delete),
    # ~/depart/[nid]/edit/ 正则
    # nid参数可传给view函数
    path('depart/<int:nid>/edit/',  depart.depart_edit),

    path('user/list/',user.user_list),
    path('user/add/',user.user_add),
    path('user/<int:nid>/edit/',  user.user_edit),
    path('user/<int:nid>/delete/',user.user_delete),

    path('pretty/list/',pretty.pretty_list),
    path('pretty/add/',pretty.pretty_add),
    path('pretty/<int:nid>/edit/',  pretty.pretty_edit),
    path('pretty/<int:nid>/delete/',  pretty.pretty_delete),

    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path("admin/<int:nid>/edit/",admin.admin_edit),

    path('login/',account.login),
    path('logout/',account.logout),

    path('order/list/',order.order_list),


    ###################图书管理视图#######################
    path('book/list/',book.book_list),
    path('book/<int:nid>/delete/', book.book_delete),
    path('book/add/',book.book_add),
    path("book/<int:nid>/edit/",book.book_edit),

    
    path('reader/list/',reader.reader_list),
    path('reader/<int:nid>/delete/', reader.reader_delete),
    path("reader/<int:nid>/edit/",reader.reader_edit),
    path('reader/add/',reader.reader_add),


    path("borrow/list/",borrow.borrow_list),
    path("borrow/outdate/",borrow.outdate_list),
    path("borrow/add/",borrow.borrow_add),
    path("borrow/<int:nid>/<str:bookname>/return/",borrow.borrow_return),
    path("borrow/<int:nid>/return/",borrow.borrow_continue),

    path("index/",mainpage.mainpage)
]
