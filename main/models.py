from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    origin_id = models.IntegerField(unique=True)
    degree = models.DecimalField(max_digits=60, decimal_places=2, default=0)
    is_student = models.BooleanField(default=True)
    # qr_code = models.ImageField(upload_to='user_qr_code/')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.origin_id}"
    

class AddedDegree(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    before_degree = models.DecimalField(max_digits=60, decimal_places=2, default=0)
    added_degree = models.DecimalField(max_digits=60, decimal_places=2)
    after_degree = models.DecimalField(max_digits=60, decimal_places=2, default=0)


class EnterExit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enter_exit')
    in_out = models.BooleanField(default=True)
    enter_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)


class UsedDegree(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    enter_exit = models.ForeignKey(EnterExit, on_delete=models.SET_NULL, null=True)
    before_degree = models.DecimalField(max_digits=60, decimal_places=2, default=0)
    used_degree = models.DecimalField(max_digits=60, decimal_places=2)
    after_degree = models.DecimalField(max_digits=60, decimal_places=2, default=0)


class TimePrice(models.Model):
    price = models.DecimalField(max_digits=60, decimal_places=2)


class Files(models.Model):
    file = models.FileField(upload_to='excell/')


class CompanyComponent(models.Model):
    logo = models.ImageField(upload_to='company_components/')
    company_name = models.CharField(max_length=255)
    about = models.TextField(blank=True, null=True)


# <----------------------------Not student users--------------------------------->


class Pc(models.Model):
    number = models.PositiveIntegerField()
    status = models.IntegerField(choices=((1, "buzy"), (2, 'blank'), (3, 'broken')), default=2)


class TimeMoney(models.Model):
    price = models.DecimalField(max_digits=60, decimal_places=2)
    for_student = models.BooleanField(default=False)


class OnOfTime(models.Model):
    pc = models.ForeignKey(Pc, on_delete=models.SET_NULL, null=True)
    pay_for = models.ForeignKey(TimeMoney, on_delete=models.SET_NULL, null=True)
    on_time = models.DateTimeField()
    off_time = models.DateTimeField(null=True, blank=True)


class Money(models.Model):
    pc = models.ForeignKey(Pc, on_delete=models.SET_NULL, null=True)
    time = models.ForeignKey(OnOfTime, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=60, decimal_places=2)
