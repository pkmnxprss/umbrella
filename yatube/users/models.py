from django.db import models
from django.contrib.auth.models import AbstractUser


# This model behaves identically to the default django user model.
# We will be able to customize it in the future if the need arises
class User(AbstractUser):
    pass
