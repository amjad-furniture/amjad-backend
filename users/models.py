from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model with unique username as the primary identifier.
    """
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True, null=True)


    # email = None
    first_name = None
    last_name = None
    date_joined = None

    USERNAME_FIELD = "username"  
    REQUIRED_FIELDS =["email"]
    def __str__(self):
        return str(self.username)


