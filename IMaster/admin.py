from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Course)
admin.site.register(Info)
admin.site.register(StudentCourseProgress)
admin.site.register(Topic)
admin.site.register(File)