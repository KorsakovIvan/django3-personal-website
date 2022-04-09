from django.db import models
from django.contrib.auth.models import User


class Priority(models.IntegerChoices):
    HIGH = 1, 'High'
    MEDIUM = 2, 'Medium'
    LOW = 3, 'Low'


class Status(models.TextChoices):
    TODO = 'to_do', 'To Do'
    IN_PROGRESS = 'in_progress', 'In Progress'
    DONE = 'done', 'Done'


class ToDo(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    title = models.CharField(
        max_length=140,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.TODO,
    )
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    deadline = models.DateField(
        null=True,
        blank=True,
    )
    completed_on = models.DateTimeField(
        null=True,
        blank=True,
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.title} by {self.assigned_to}"
