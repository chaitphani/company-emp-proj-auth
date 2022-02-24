from django.db import models
import uuid
import datetime


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_title = models.CharField(max_length=200, blank=False, null=False)
    project_description = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    project_deadline_date = models.DateField("Date", default=datetime.date.today)
    comments = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.project_title
