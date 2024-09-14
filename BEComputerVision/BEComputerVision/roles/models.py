from django.db import models
from BEComputerVision.users.models import Users
from BEComputerVision.projects.models import Projects
import uuid

class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    role_user = models.CharField(max_length=255)
