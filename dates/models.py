from django.db import models

from users.models import Developer

from tasks.models import Task


class Date(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
