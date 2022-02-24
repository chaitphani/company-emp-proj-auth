from django.db import models
from super_admin.models import User
import uuid


class Company(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=200, blank=False, null=False)
    company_address = models.CharField(max_length=200, blank=False, null=False)
    company_email = models.CharField(max_length=200, blank=False, null=False)
    company_phonenumber = models.CharField(max_length=200, blank=False, null=False)
    company_website = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    
    user = models.ForeignKey(
        User,
        related_name="company_admin",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.company_name
