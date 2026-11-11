
from django.db import transaction

from departments.models import Department


@transaction.atomic
def save_department(*, department):

    old_logo_name = None

    if department.pk:
        old_department = Department.objects.filter(
            pk=department.pk
        ).first()

        if old_department is None:
            raise Department.DoesNotExist

        if old_department.logo:
            old_logo_name = old_department.logo.name

    department.full_clean()
    department.save()

    new_logo_name = department.logo.name if department.logo else None

    if old_logo_name and old_logo_name != new_logo_name:

        storage = department._meta.get_field("logo").storage

        transaction.on_commit(
            lambda: storage.delete(old_logo_name)
        )

    return department


@transaction.atomic
def delete_department(*, department):


    logo_name = department.logo.name if department.logo else None
    storage = department._meta.get_field("logo").storage

    department.delete()

    # Delete the logo only after successful database commit.
    if logo_name:
        transaction.on_commit(
            lambda: storage.delete(logo_name)
        )
