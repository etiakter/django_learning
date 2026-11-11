from django.db import models
# for image name
import os
from django.utils.text import slugify

def department_logo_path(instance, filename):
    extension=os.path.splitext(filename)[1].lower()
    name=slugify(instance.name)
    return f"depatments/{name}{extension}"

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=150, unique=True)
    description=models.TextField(blank=True, null=True)
    logo=models.ImageField(upload_to=department_logo_path, null=True, blank=True)

    
    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name