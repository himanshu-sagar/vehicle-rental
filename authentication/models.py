from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid


class User(AbstractUser):
    """
    Creating custom user model for making Phone as default username field
    """
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(max_length=15, primary_key=True, validators=[phone_regex])
    is_store_manager = models.BooleanField(default=False, auto_created=True)
    is_customer = models.BooleanField(default=False, auto_created=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.phone)

    def is_store_manager(self):
        return self.is_store_manager

    def is_customer(self):
        return self.is_customer