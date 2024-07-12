from django.contrib import admin
from .models import Trainer, Student, Bar, BarSold, Tariffs

admin.site.register(Tariffs)
admin.site.register(Trainer)
admin.site.register(Student)
admin.site.register(Bar)
admin.site.register(BarSold)