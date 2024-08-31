from django.db import models
from BEComputerVision.users.models import Users
from BEComputerVision.projects.models import Projects

class Roles(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    role_user = models.CharField(max_length=255)
