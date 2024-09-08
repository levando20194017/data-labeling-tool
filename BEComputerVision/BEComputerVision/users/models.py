from django.db import models
import uuid

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(default= '', max_length=20, null=True, blank=True)
    address = models.CharField(default= '', max_length=255, null=True, blank=True)
    img_url = models.CharField(default= '', max_length=255, null=True, blank=True)
    role = models.CharField(default="member", max_length=20)
    is_verified = models.BooleanField(default=False)