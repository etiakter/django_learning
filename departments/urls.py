
from django.urls import path

from departments.views import (
    DepartmentListView,
    DepartmentCreateView,
    DepartmentDetailView,
    DepartmentUpdateView,
    DepartmentDeleteView,
)


app_name = "departments"


urlpatterns = [

    path(
        "department_list",
        DepartmentListView.as_view(),
        name="department_list"
    ),

    path(
        "create/",
        DepartmentCreateView.as_view(),
        name="department_create"
    ),

    path(
        "<int:pk>/",
        DepartmentDetailView.as_view(),
        name="department_detail"
    ),

    path(
        "<int:pk>/update/",
        DepartmentUpdateView.as_view(),
        name="department_update"
    ),

    path(
        "<int:pk>/delete/",
        DepartmentDeleteView.as_view(),
        name="department_delete"
    ),

]
