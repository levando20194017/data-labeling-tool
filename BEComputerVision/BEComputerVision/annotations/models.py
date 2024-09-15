from django.db import models
from BEComputerVision.users.models import Users
from BEComputerVision.projects.models import Projects
from BEComputerVision.images.models import ImagesProjects
import uuid

class Annotations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagesProjects, on_delete=models.CASCADE)
    data_url = models.CharField(max_length=255)
