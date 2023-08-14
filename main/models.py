from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    origin_id = models.IntegerField(unique=True)
    degree = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.origin_id}"
    

class AddedDegree(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    before_degree = models.IntegerField(default=0)
    added_degree = models.IntegerField()
    after_degree = models.IntegerField(default=0)


class UsedDegree(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    before_degree = models.IntegerField(default=0)
    used_degree = models.IntegerField()
    after_degree = models.IntegerField(default=0)


class EnterExit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enter_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    

class TimePrice(models.Model):
    price = models.DecimalField(max_digits=60, decimal_places=2)

    def __str__(self) -> str:
        return self.price
