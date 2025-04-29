from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'hr/employee_list.html', {'employees': employees})
