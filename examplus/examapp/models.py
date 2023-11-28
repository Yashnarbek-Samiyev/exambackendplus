from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        permissions = (
            ("can_do_something", "Can do something"),
        )


class MyGroup(models.Model):
    members = models.ManyToManyField(CustomUser, related_name='my_groups')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'groups'


class MyPermission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'permission')

    def __str__(self):
        return f"{self.user} - {self.permission}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class ProductAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product)
    viewed_status = models.BooleanField(default=False)
    viewing_time_seconds = models.IntegerField(default=0)


class LessonView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_status = models.BooleanField(default=False)
    viewing_time_seconds = models.IntegerField(default=0)
    last_viewed_date = models.DateTimeField(auto_now_add=True)
