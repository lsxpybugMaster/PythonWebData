from django.shortcuts import render,redirect
from django import forms
from app01 import models

class LoginForm(forms.Form):
    username = forms.CharField(
        label = "username",
        widget = forms.TextInput(attrs={"class":"form-control","id":'floatingInput','placeholder':"Username"}),
        required=True,
    )
    passward = forms.CharField(
        label = "passward",
        widget = forms.PasswordInput(attrs={"class":"form-control","id":'floatingPassword', 'placeholder':"Password"}),
        required=True,
    )
    


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form' : form})

    form = LoginForm(data = request.POST)
    if form.is_valid():
        # cleaned_data
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            msg = "用户名或密码错误"
            return render(request,'login.html',{"form":form,"msg":msg})
        
        # cookie设置
        request.session['info'] = admin_object.username
        return redirect('/index/')

    return render(request,'login.html',{"form":form})


def logout(request):
    request.session.clear()
    return redirect("/login/")