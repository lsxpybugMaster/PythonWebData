from math import ceil
from django.utils.safestring import mark_safe
import copy

class Pagination():
    '''
    <nav aria-label="Page navigation example" style="margin-top: 15px;">
        <ul class="pagination justify-content-center"> 
        {{safestring}}
        </ul>
    </nav>
    '''
    def __init__(self,request,queryset,page_size = 10,page_param = 'page',plus = 5):
        
        # 获取之前的查询输入
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        # 获取页码
        page = request.GET.get(page_param,"1")
        page = int(page) if page.isdecimal() else 1

        self.page = page
        self.page_size = page_size #每页展示多少数据

        # 计算首页和尾页
        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 获取对应的查询数据
        self.page_queryset = queryset[self.start:self.end]

        # 获取需要展示的总页数
        total_count = queryset.count()
        self.total_page_count = ceil(total_count/page_size)

        # 决定当前页的前多少项页码进行展示
        self.plus = plus
 
    def html(self):
        # 一共展示多少页码
        page_show = 2 * self.plus + 1 

        # 当前数据库中页面较少
        if self.total_page_count <= page_show:
            start_page = 1
            end_page = self.total_page_count
        # 数据库中页面多，且当前页码数较小无法展示前plus项
        elif self.page <= self.plus:
            start_page = 1
            end_page = page_show
        # 数据库中页面多，且当前页码数较大无法展示后plus项
        elif (self.page + self.plus) > self.total_page_count:
            start_page = self.total_page_count - page_show + 1
            end_page   = self.total_page_count
        else:
            start_page = self.page - self.plus
            end_page   = self.page + self.plus

        page_str_list = []
        # 在之前的查询基础上补充后续: &page=1
        self.query_dict.setlist(self.page_param,[1])
        # 加入首页html
        page_str_list.append(f'<li class="page-item"><a class="page-link" href="?{self.query_dict.urlencode()}">首页</a></li>')

        # 加入上一页html
        if self.page > 1:
            self.query_dict.setlist(self.page_param,[self.page - 1])
            prev = f'<li class="page-item"><a class="page-link" href="?{self.query_dict.urlencode()}">上一页</a></li>'
        else:
            prev = f'<li class="page-item disabled"><a class="page-link">上一页</a></li>'

        page_str_list.append(prev)

        # 加入其余页html
        for i in range(start_page,end_page + 1):
            self.query_dict.setlist(self.page_param,[i])
            if i == self.page:
                ele = f'<li class="page-item active"><a class="page-link" href="?{self.query_dict.urlencode()}">{i}</a></li>'
            else:
                ele = f'<li class="page-item"><a class="page-link" href="?{self.query_dict.urlencode()}">{i}</a></li>'
            page_str_list.append(ele)
        
        # 加入下一页html
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param,[self.page + 1])
            prev = f'<li class="page-item"><a class="page-link" href="?{self.query_dict.urlencode()}">下一页</a></li>'
        else:
            prev = f'<li class="page-item disabled"><a class="page-link">下一页</a></li>'
        page_str_list.append(prev)

        # 加入尾页html
        self.query_dict.setlist(self.page_param,[self.total_page_count])
        page_str_list.append(f'<li class="page-item"><a class="page-link" href="?{self.query_dict.urlencode()}">尾页</a></li>')

        # 加入查找的string
        search_string = '''
        <li>
            <form style="float:left ; margin-left: 3px;" method="get">
                <input name="page" style="position: relative; float: left; width: 80px; border-radius: 0px;"
                type = 'text' class = 'form-control' placeholder="页码">
                <button class="btn btn-primary" type="submit">跳转</button>
            </form>
        </li>
        '''

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))

        # 返回html代码
        return page_string