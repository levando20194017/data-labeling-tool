from django.db import models
from users.models import Users
from projects.models import Projects
from images.models import ImagesProjects

class Annotations(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagesProjects, on_delete=models.CASCADE)
    data_url = models.CharField(max_length=255)
