from django.db import models
from BEComputerVision.projects.models import Projects
import uuid

class Versions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
