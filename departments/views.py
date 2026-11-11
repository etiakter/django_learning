
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from departments.models import Department
from departments.forms import DepartmentForm

from departments.selectors.department_selector import (
    get_department_list,
    get_department_by_id,
)

from departments.services.department_service import (
    save_department,
    delete_department,
)


# Reusable mixin for retrieving a department
class DepartmentObjectMixin:

    def get_object(self, queryset=None):

        department = get_department_by_id(
            department_id=self.kwargs["pk"]
        )

        if department is None:
            raise Http404("Department not found.")

        return department


# Reusable mixin for creating and updating departments
class DepartmentFormServiceMixin:

    def form_valid(self, form):

        try:
            self.object = save_department(
                department=form.save(commit=False)
            )

        except ValidationError as error:
            form.add_error(None, error)
            return self.form_invalid(form)

        messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())


# 1. Department List
class DepartmentListView(ListView):

    model = Department
    template_name = "departments/department_list.html"
    context_object_name = "departments"
    paginate_by = 10

    def get_queryset(self):

        search = self.request.GET.get("q", "")

        return get_department_list(search=search)


# 2. Department Create
class DepartmentCreateView(
    DepartmentFormServiceMixin,
    CreateView
):

    model = Department
    form_class = DepartmentForm
    template_name = "departments/department_form.html"
    success_url = reverse_lazy("departments:department_list")

    success_message = "Department created successfully."


# 3. Department Detail
class DepartmentDetailView(
    DepartmentObjectMixin,
    DetailView
):

    model = Department
    template_name = "departments/department_detail.html"
    context_object_name = "department"


# 4. Department Update
class DepartmentUpdateView(
    DepartmentObjectMixin,
    DepartmentFormServiceMixin,
    UpdateView
):

    model = Department
    form_class = DepartmentForm
    template_name = "departments/department_form.html"
    context_object_name = "department"

    success_message = "Department updated successfully."

    def get_success_url(self):

        return reverse_lazy(
            "departments:department_detail",
            kwargs={"pk": self.object.pk}
        )


# 5. Department Delete
class DepartmentDeleteView(
    DepartmentObjectMixin,
    DeleteView
):

    model = Department
    template_name = "departments/department_confirm_delete.html"
    success_url = reverse_lazy("departments:department_list")

    def form_valid(self, form):

        department = self.object

        delete_department(department=department)

        messages.success(
            self.request,
            "Department deleted successfully."
        )

        return HttpResponseRedirect(self.get_success_url())
