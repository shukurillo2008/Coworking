from django.contrib import admin
from . import models

admin.site.register(models.Student)
admin.site.register(models.EnterExit)
admin.site.register(models.AddedDegree)
admin.site.register(models.UsedDegree)
admin.site.register(models.TimePrice)
admin.site.register(models.Files)