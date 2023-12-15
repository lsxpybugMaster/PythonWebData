from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):
        #排除那些不需要登录就能访问的页面
        if request.path_info == '/login/':
            return

        #读取当前访问用户的session信息
        info_dict = request.session.get("info")
        if info_dict:
            return
        
        #若用户未登录
        return redirect("/login/")
