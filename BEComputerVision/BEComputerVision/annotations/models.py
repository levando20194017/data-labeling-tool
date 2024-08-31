from django.db import models
from BEComputerVision.users.models import Users
from BEComputerVision.projects.models import Projects
from BEComputerVision.images.models import ImagesProjects

class Annotations(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagesProjects, on_delete=models.CASCADE)
    data_url = models.CharField(max_length=255)
