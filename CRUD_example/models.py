from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            email = email,
            password = password,
            **extra_fields,
        )

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Login(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Software(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField(max_length=512)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CustomerSoftware(models.Model):
    cid = models.ForeignKey("Customer", on_delete=models.CASCADE)
    sid = models.ForeignKey("Software", on_delete=models.CASCADE)
    date_obtained = models.DateTimeField(auto_now=True)