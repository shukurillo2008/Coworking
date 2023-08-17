from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    origin_id = models.IntegerField(unique=True)
    degree = models.DecimalField(max_digits=60, decimal_places=2, default=0)
    qr_code = models.ImageField(upload_to='user_qr_code/')

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

