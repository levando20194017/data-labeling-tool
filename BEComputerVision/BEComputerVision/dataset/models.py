from django.db import models
from BEComputerVision.projects.models import Projects
from BEComputerVision.images.models import ImagesProjects
from BEComputerVision.annotations.models import Annotations

class Dataset(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagesProjects, on_delete=models.CASCADE)
    annotation = models.ForeignKey(Annotations, on_delete=models.CASCADE)
