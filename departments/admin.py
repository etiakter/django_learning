from django.contrib import admin
from departments.models import Department
from django.utils.html import format_html
# Register your models here.
# admin.site.register(Department)
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('id','name','description','logo_preview',)
    search_fields=('name','description')
    ordering=('name',)
    list_filter=('name',)
    list_per_page=5

    @admin.display(description="Department logo")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="80" height="60" style="object-fit: contain;" />',
                obj.logo.url
            )
        return "No logo"
