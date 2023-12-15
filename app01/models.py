from django.db import models

# Create your models here.

class Admin(models.Model):
    '''管理员表'''
    username = models.CharField(verbose_name="用户名",max_length=32)
    passward = models.CharField(verbose_name="密码",max_length=64)
    
class UserInfo(models.Model):
    '''员工表'''
    name = models.CharField(verbose_name="姓名",max_length=16)
    passward = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    # 外码约束 , 以及完整性约束
    # models.CASCADE 级联删除
    # models.SET_NULL 置空
    depart = models.ForeignKey(to="Departments",to_field="id",on_delete=models.CASCADE)
    
    gender_choices = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)


class Departments(models.Model):
    '''部门表'''
    title = models.CharField(verbose_name="标题" ,max_length=32)

    def __str__(self):
        return self.title
    
    
class PrettyNum(models.Model):
    '''靓号表'''
    mobile = models.CharField(verbose_name="手机号",max_length=11)

    price = models.IntegerField(verbose_name="价格",default=0)

    level_choices = (
        (1,"S"),
        (2,"A"),
        (3,"B"),
        (4,"C"),
    )

    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices,default=4)

    status_choices = (
        (1,"已占有"),
        (2,"未使用"),
    )

    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=2)

# js ajax测试用model
class Order(models.Model):
    '''订单表'''
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="名称",max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )

    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=1)
    admin = models.ForeignKey(verbose_name="管理员",to="Admin",on_delete=models.CASCADE)



class Book(models.Model):
    '''图书表'''
    # 书号自动生成
    title = models.CharField(verbose_name="书名",max_length=32)
    author = models.CharField(verbose_name="作者",max_length=32)
    publisher = models.CharField(verbose_name="出版商",max_length=32)
    time = models.DateField(verbose_name="出版日期")
    bookleft = models.IntegerField(verbose_name="在馆图书")
    booktotal = models.IntegerField(verbose_name="总数")

    def __str__(self):
        return self.title

class Reader(models.Model):
    '''读者表'''
    name = models.CharField(verbose_name="姓名",max_length=16)
    gender_choices = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)
    departname = models.CharField(verbose_name="系名",max_length=32)
    grade =  models.IntegerField(verbose_name="年级")

    def __str__(self):
        return self.name

class Borrow(models.Model):
    '''借阅表'''
    book = models.ForeignKey(verbose_name="书名",to="Book",to_field="id",on_delete=models.CASCADE)
    reader = models.ForeignKey(verbose_name="借阅人",to="Reader",to_field="id",on_delete=models.CASCADE)
    borrow_date = models.DateField(verbose_name="借阅日期")
    return_date = models.DateField(verbose_name="应还日期")
    renewed = models.IntegerField(verbose_name="续借",default=0)

