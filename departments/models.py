from django.db import models
# for image name
import os
from django.utils.text import slugify
import uuid

def department_logo_path(instance, filename):
    extension=os.path.splitext(filename)[1].lower()
    name=slugify(instance.name)
    # unique_id = uuid.uuid4().hex[:8]
    unique_id = uuid.uuid4().hex
    return f"departments/{name}_{unique_id}{extension}"

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=150, unique=True)
    description=models.TextField(blank=True, null=True)
    logo=models.ImageField(upload_to=department_logo_path, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name