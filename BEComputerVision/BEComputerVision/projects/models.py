from django.db import models
from BEComputerVision.users.models import Users
import uuid

class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

