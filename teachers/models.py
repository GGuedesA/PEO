from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils import timezone
from .managers import TeacherManager

class Teacher(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    age = models.PositiveBigIntegerField(null=True)
    description = models.TextField(null=True)
    hourly_price = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    
    objects = TeacherManager()
    
    groups = models.ManyToManyField(
        Group,
        related_name='teacher_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='teacher_permissions',
        blank=True
    )
    
    def __str__(self):
        return self.email
    