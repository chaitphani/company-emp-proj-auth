from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class UserManager(BaseUserManager):
    def create_superuser(self, **kwargs):
        user = self.model(email=kwargs["email"])
        user.set_password(kwargs["password"])
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    class UserTypes(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        COMPANY_ADMIN = "COMPANY_ADMIN", "company_admin"
        EMPLOYEE = "EMPLOYEE", "employee"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    phone = PhoneNumberField(blank=True, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    user_type = models.CharField(max_length=200, choices=UserTypes.choices)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
