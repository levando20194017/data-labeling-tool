from django.db import models
from projects.models import Projects
from images.models import ImagesProjects
from annotations.models import Annotations

class Dataset(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagesProjects, on_delete=models.CASCADE)
    annotation = models.ForeignKey(Annotations, on_delete=models.CASCADE)
