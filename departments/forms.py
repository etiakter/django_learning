from django import forms
from departments.models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = [
            "name", 
            "description", 
            "logo","is_active"
        ]

        widgets={
            'name':
            forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter department name'
            }),

            'description':
            forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Enter department description',
                'rows':4
            }),
            'logo':
            forms.ClearableFileInput(attrs={
                'class':'form-control'
            })
        }

    # def clean_name(self):
    #     name = self.cleaned_data["name"].strip()

    #     if not name:
    #         raise forms.ValidationError("Department name is required.")

    #     queryset = Department.objects.filter(name__iexact=name)

    #     if self.instance.pk:
    #         queryset = queryset.exclude(pk=self.instance.pk)

    #     if queryset.exists():
    #         raise forms.ValidationError(
    #             "This department already exists."
    #         )

    #     return name