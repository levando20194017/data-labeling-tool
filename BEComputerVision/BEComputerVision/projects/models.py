from django.db import models
from BEComputerVision.users.models import Users

class Projects(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

