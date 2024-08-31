from django.db import models
from BEComputerVision.projects.models import Projects

class Versions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
