from django.db import models

from users.models import Developer

from projects.models import Project


class Date(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
