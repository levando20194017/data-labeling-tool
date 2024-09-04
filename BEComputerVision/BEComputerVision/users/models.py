from django.db import models

class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    img_url = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)