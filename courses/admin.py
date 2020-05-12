from django.contrib import admin
from .models import Course, Department, Lecture, Edition

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Edition)
admin.site.register(Lecture)