from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    diagnosis_record = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(null=True, blank=True)
    previous_diagnosis_value = models.IntegerField(default=-1, null=True, blank=True)
    previous_diagnosis_class = models.CharField(max_length=100, default='None')