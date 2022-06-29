# 'models' contains all of the model types and model fields
from django.db import models

from django.contrib.auth.models import (
    # 'BaseUserManager' is a manager for customizing django's built in 'User' object
    BaseUserManager,
    # 'AbstractBaseUser' is the base class for an abstract 'User'. Extending this allows
    # for editing the fields of the built in 'User' object. The benefit of this is we can
    # use django's built in authentication for custom 'User' objects.
    AbstractBaseUser,
)

# 'UserManager' is a 'BaseUserManager'
# 'UserManager' helps manage 'User' objects
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

# 'User' is an 'AbstractBaseUser'
# 'User' is overriding the built in 'User' object so that it can be customized
class User(AbstractBaseUser):
    # Users must have unique emails
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)

    # Define which field will be treated like the username. Must be unique.
    USERNAME_FIELD = 'email'
    # Required fields other than the field treated like the username
    REQUIRED_FIELDS = []

    # Set the object manager
    objects = UserManager()

    # Define the object's string representation
    def __str__(self):
        return self.email

# 'Login' is a 'Model'
# 'Login' is a model used for logging in a user.
# It is used purely for defining a form structure, so the table should not
# be populated with any instances
class Login(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

# 'Customer' is a 'Model'
# The 'Customer' table holds all customer objects
class Customer(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 'Software' is a 'Model'
# The 'Software' table holds all software objects
class Software(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField(max_length=512)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 'CustomerSoftware' is a 'Model'
# The 'CustomerSoftware' table holds all relations between a 'Customer' and a 'Software'
class CustomerSoftware(models.Model):
    cid = models.ForeignKey("Customer", on_delete=models.CASCADE)
    sid = models.ForeignKey("Software", on_delete=models.CASCADE)
    date_obtained = models.DateTimeField(auto_now=True)