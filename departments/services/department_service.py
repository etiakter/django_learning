from django.db import transaction
from departments.models import Department

@transaction.Atomic
def save_department(*, department):

    old_logo_name=None
    if department.pk:
        old_department=Department.objects.filter(
           pk=department.pk 
        ).first
    if old_department is None:
        raise Department.DoesNotExist


    department.full_clean()
    department.save()

    
    if old_department.logo and department.logo:
        old_logo_name=old_department.logo.name      
        storage=old_department._meta.get_field('logo').storage

        transaction.on_commit(
           lambda:storage.delete(old_logo_name) 
        )


