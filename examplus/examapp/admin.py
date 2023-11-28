from django.contrib import admin
from .models import CustomUser, Product, ProductAccess, Lesson, LessonView

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(ProductAccess)
admin.site.register(Lesson)
admin.site.register(LessonView)


# Register your models here.
