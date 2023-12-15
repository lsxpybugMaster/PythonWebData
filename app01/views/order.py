
from django.shortcuts import render
from app01 import models
from app01.utils.bootstrap import BootstrapModelForm

class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ['oid']

def order_list(request):
    form = OrderModelForm()
    return render(request,"order_list.html",{"form" : form})

