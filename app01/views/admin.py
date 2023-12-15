from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination

from app01.utils.form import BootstrapModelForm
from app01.utils.encrypt import md5
from django import forms


def admin_list(request):

    data_dict = {}
    search_data = request.GET.get("q","")
    if search_data: 
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    page_obj = Pagination(request,queryset,page_size=3)

    return render(request,"admin_list.html",{"queryset" : page_obj.page_queryset,
                                             "safestring" : page_obj.html()})

class AdminModelForm(BootstrapModelForm):
    
    confirm_passward = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username","passward","confirm_passward"]
        widgets = {
            "passward" : forms.PasswordInput(render_value=True)
        }

    ############################## 有关密码加密 ############################## 
    # def clean_passward(self):
    #     pwd = self.cleaned_data.get("passward")
    #     return md5(pwd)

    # 钩子方法，用于校验密码与确认密码是否一致
    # def clean_confirm_passward(self):
    #     pwd = self.cleaned_data.get("passward")
    #     confirm = md5(self.cleaned_data.get("confirm_passward"))
    #     if confirm != pwd:
    #         raise ValidationError("密码不一致")
    #     # 确认密码无误后，加密存取密码
    #     return confirm #md5(confirm)
    ############################## 有关密码加密 ############################## 

    # 钩子方法，用于校验密码与确认密码是否一致
    def clean_confirm_passward(self):
        pwd = self.cleaned_data.get("passward")
        confirm = self.cleaned_data.get("confirm_passward")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 确认密码无误后，加密存取密码
        return confirm 

class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

def admin_add(request):
    '''添加管理员'''
    title = "新建管理员"

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request,"change.html",{"form" : form , "title" : title})
    
    form = AdminModelForm(data = request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    
    return render(request,"change.html",{"form" : form , "title" : title})

def admin_edit(request,nid):

    row_object = models.Admin.objects.filter(id = nid).first()
    if not row_object:
        return redirect("/admin/list/")
    
    title = "编辑管理员"

    if(request.method == 'GET'):
        form = AdminEditModelForm(instance = row_object)
        return render(request,'change.html',{'form': form , 'title':title})
    
    form = AdminEditModelForm(data = request.POST ,instance = row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    
    return render(request,'change.html',{'form': form , 'title':title})