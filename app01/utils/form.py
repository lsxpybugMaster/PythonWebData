from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.bootstrap import BootstrapModelForm

class UserModelForm(BootstrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name","passward","age","account","create_time","depart","gender"]

class PrettyModelForm(BootstrapModelForm):
    # 手机号字符串正则校验
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误'),],
    )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

      # 钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        exists = models.PrettyNum.objects.filter(mobile = txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        return txt_mobile

class PrettyEditModelForm(BootstrapModelForm):

    mobile = forms.CharField(disabled=True, label="手机号(不可修改)")

    class Meta:
        model = models.PrettyNum
        fields = "__all__"