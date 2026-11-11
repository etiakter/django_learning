from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from  .models import Student
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.http import require_POST

#for export excel and pdf
from io import BytesIO

from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from copy import copy
from datetime import datetime
from django.utils import timezone
from openpyxl.styles import Alignment
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def home(request):

    return render(request,'home.html')

def student_list(request):
    search_query = request.GET.get("search", "").strip()    
    students=Student.objects.all().order_by('id')

    if search_query:
        students=students.filter(
            Q(name__contains=search_query) | Q(email__contains=search_query)
        )

    paginator=Paginator(students,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    context={
        'students':page_obj,
        'page_obj':page_obj,
        'search_query':search_query
    }
    return render(request, 'students/student_list.html', context)
def student_create(request):
    if request.method=="POST":
        name=request.POST.get("name","").strip()
        email=request.POST.get("email","").strip()
        age=request.POST.get("age")

        if Student.objects.filter(email__iexact=email).exists():
            messages.warning(request,"This email address is already registered! Please use another email.")
            return redirect('student_create')
        try:
            Student.objects.create(
                    name=name,
                    email=email,
                    age=age
                )
            messages.success(request,"Student added successfully")
            return redirect('student_create')
        except :
            messages.error(request,
                "Unable to save the student. Please try again.")
            return redirect("student_create")
    return render(request, 'students/student_form.html')

def student_update(request,id):
    student=get_object_or_404(Student, pk=id)
    if request.method=="POST":
        name=request.POST.get("name","").strip()
        email=request.POST.get("email","").strip()
        age=request.POST.get("age")

        if not name or not email:
            messages.error(request, "Please enter both name and email.")
            return redirect("student_update", id=student.pk)
        if Student.objects.filter(email__iexact=email).exclude(id=student.pk).exists():
            messages.error(request,"This email already exists.")
            return redirect("student_update", id=student.pk)
        try:
            student.name=name
            student.email=email
            student.age=age
            student.save()
            return redirect("student_list")
        except IntegrityError:
            messages.error(request,"This email is already in use.")
            return redirect("student_update", id=student.pk)
    return render(request,"students/student_update.html",
        {"student": student})

@require_POST
def student_delete(request, id):
    student=get_object_or_404(Student, pk=id)
    try:
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect("student_list")
    except :
        messages.error("There is a problem to delete data.")
        redirect('student_list')
        
def export_students_excel(request):
    students = Student.objects.all().order_by("id")
    total_students = students.count()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Students"

    # Report title and summary
    worksheet.append(["Student List Report"])
    worksheet.append(["Report Generated", timezone.localtime().strftime("%d-%m-%Y %I:%M %p")])
    worksheet.append(["Total Students", total_students])
    worksheet.append([])

    # Table headings
    worksheet.append(["ID", "Name", "Email","Age"])

    # Student records
    for student in students:
        worksheet.append([
            student.id,
            student.name,
            student.email,
            student.age,
        ])

    # Format title and headings
    worksheet["A1"].font = worksheet["A1"].font.copy(
        bold=True, size=16
    )

    for cell in worksheet[5]:
        cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
         )
        font = copy(cell.font)
        font.bold = True
        cell.font = font
    # Center ID, Name, and Email columns
    for row in worksheet.iter_rows(min_row=6, max_row=worksheet.max_row):
        for cell in row[:3]:
            cell.alignment = Alignment(horizontal="center")
            
    worksheet.column_dimensions["A"].width = 22
    worksheet.column_dimensions["B"].width = 25
    worksheet.column_dimensions["C"].width = 35
    worksheet.column_dimensions["D"].width = 22

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )
    response["Content-Disposition"] = (
        'attachment; filename="students.xlsx"'
    )

    workbook.save(response)
    return response


def export_students_pdf(request):
    students = Student.objects.all().order_by("id")
    total_students = students.count()

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        title="Student List Report",
    )

    styles = getSampleStyleSheet()

    elements = [
        Paragraph("Student List Report", styles["Title"]),
        Paragraph(
            f"Report Generated: "
            f"{timezone.localtime().strftime('%d-%m-%Y %I:%M %p')}",
            styles["Normal"],
        ),
        Paragraph(
            f"Total Students: {total_students}",
            styles["Heading2"],
        ),
    ]

    # Add some space before the table
    # from reportlab.platypus import Spacer
    elements.append(Spacer(1, 15))

    # Table headings
    data = [["ID", "Name", "Email", "Age"]]

    for student in students:
        data.append([
            str(student.id),
            str(student.name),
            str(student.email),
            str(student.age),
        ])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 15),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    elements.append(table)
    pdf.build(elements)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/pdf",
    )
    response["Content-Disposition"] = (
        'attachment; filename="students.pdf"'
    )

    buffer.close()
    return response


    
