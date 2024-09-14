from django.db import models
from BEComputerVision.projects.models import Projects
from BEComputerVision.images.models import ImagesProjects
from BEComputerVision.annotations.models import Annotations
import uuid

class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagesProjects, on_delete=models.CASCADE)
    annotation = models.ForeignKey(Annotations, on_delete=models.CASCADE)
