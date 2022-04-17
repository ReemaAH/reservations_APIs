from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from .managers import UserManager


class CustomUser(AbstractUser):
    '''
    CustomUser Model:
    This model is to override the default user model
    '''

    username = None
    email = None
    employee_number = models.CharField(
        max_length=4, unique=True, blank=False, null=False, validators=[MinLengthValidator(4)])

    ADMIN = 1
    EMPLOYEE = 2
    ROLE_CHOICES = (
          (ADMIN, 'Admin'),
          (EMPLOYEE, 'Employee'),
      )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'employee_number'
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(
        ('active'),
        default=True
    )

    objects = UserManager()
    def __str__(self):
        return self.first_name + "" + self.last_name
