from django.db.models import Q
from departments.models import Department

def get_department_list(*, search=""):
    queryset=Department.objects.all()
    search=search.strip()

    if search:
       queryset= queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    return queryset

def get_department_id(*, department_id):
    return Department.objects.filter(
        pk=department_id
    ).first()
