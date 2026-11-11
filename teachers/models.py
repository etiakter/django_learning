from django.db import models
from departments.models import Department

# Create your models here.
class Teacher(models.Model):
       class Gender(models.TextChoices):
              Male='M','Male'
              Female='F','Female'
              Other='O','Other'
       employee_id=models.CharField(
              max_length=12,
              unique=True
       )
       name=models.CharField(max_length=100) 
       email=models.EmailField(unique=True)
       phone=models.CharField(
              max_length=20, 
              null=True,
              blank=True
       )
       gender=models.CharField(
              max_length=1, 
              choices=Gender.choices
        )
       picture=models.ImageField(
              upload_to='teachers/',
              blank=True, 
              null=True
       )
       date_of_birth=models.DateField()
       address=models.TextField(blank=True, null=True) 
     
       class Meta:
              ordering=["name"]
              verbose_name = 'Teacher'
              verbose_name_plural = 'Teachers'
       

       def __str__(self):
              return f"{self.employee_id} - {self.name}"

class TeacherEmploymentHistory(models.Model):
       class EmploymentType(models.TextChoices):
              FULL_TIME = 'FT', 'Full Time'
              PART_TIME = 'PT', 'Part Time'
              CONTRACT = 'CT', 'Contract'
       class EmploymentStatus(models.TextChoices):
              ACTIVE = 'A', 'Active'
              INACTIVE = 'I', 'Inactive'
              RESIGNED = 'R', 'Resigned'
              RETIRED = 'T', 'Retired'
              TERMINATED = 'X', 'Terminated'
       teacher = models.ForeignKey(
              Teacher,
              on_delete=models.PROTECT,
              related_name='employment_histories'
       )

       department = models.ForeignKey(
              Department,
              on_delete=models.PROTECT,
              related_name='teacher_employment_histories'
       )

       designation = models.CharField(max_length=100)

       salary = models.DecimalField(
              max_digits=10,
              decimal_places=2
       )

       employment_type = models.CharField(
              max_length=2,
              choices=EmploymentType.choices,
              default=EmploymentType.FULL_TIME
       )

       employment_status = models.CharField(
              max_length=1,
              choices=EmploymentStatus.choices,
              default=EmploymentStatus.ACTIVE
       )

       start_date = models.DateField()
       end_date = models.DateField(
              blank=True,
              null=True
       )
      
       created_at=models.DateTimeField(auto_now_add=True)
       updated_at=models.DateTimeField(auto_now=True)
       remarks = models.TextField(blank=True)

       class Meta:
            
              constraints=[
                     models.CheckConstraint(
                            condition=(
                                          models.Q(end_date__isnull=True)|
                                          models.Q(end_date__gte=models.F('start_date'))
                                   ),
                            name="valid_employment_dates"
                            ),

                     models.UniqueConstraint(
                            fields=['teacher'],
                            condition=models.Q(end_date__isnull=True),
                            name='one_current_employment_per_teacher'
                     )

              ]

    

       def __str__(self):
              return f"{self.teacher.name} - {self.designation}"

