
from django.urls import path
from students import views
# from students import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:id>/update/', views.student_update, name='student_update'),
    path('students/<int:id>/delete/', views.student_delete, name='student_delete'),
        
    path(
        "students/export/excel/",
        views.export_students_excel,
        name="export_students_excel",
    ),
    path(
        "students/export/pdf/",
        views.export_students_pdf,
        name="export_students_pdf",
    ),

]

