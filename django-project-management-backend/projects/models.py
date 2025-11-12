from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name="created_projects", on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="projects")
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('completed', 'Completed'), ('archived', 'Archived')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # by-default UTC time but i changed in settings.py

    def __str__(self):
        return f"{self.name} - Status : {self.status}"
