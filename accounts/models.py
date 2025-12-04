from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone):
        user = self.model(phone=phone)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'phone'