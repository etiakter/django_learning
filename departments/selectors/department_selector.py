from django.db.models import Q
from departments.models import Department

def get_department_list(*, search=""):
    