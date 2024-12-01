from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from functools import wraps
from .models import DynamicForm, FormField, Employee, FormFieldValue, Admin
from .serializer import FormFieldSerializer, EmployeeSerializer, FormFieldValueSerializer

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def login_regFuntion(request):
    return render(request, 'login_reg.html')
 
@login_required 
@api_view(['GET'])
def homePage(request):
    formfieldobjs = FormField.objects.all()
    formfield_serializer = FormFieldSerializer(formfieldobjs, many=True)

    employeeobjs = Employee.objects.all()
    employee_serializer = EmployeeSerializer(employeeobjs, many=True)
    return render(request, 'homepage.html', {'field_datas': formfield_serializer.data, 'employee_datas': employee_serializer.data})

@login_required
@api_view(['GET'])
def formFields(request):
    formfieldobjs = FormField.objects.all()
    allobjs = FormFieldSerializer(formfieldobjs, many=True)
    return render(request, 'custom_field.html', {'field_datas': allobjs.data})

@login_required
@api_view(['POST'])
def addField(request):
    if not DynamicForm.objects.exists():
        DynamicForm.objects.create(dynamicform_name="New Dynamic Form")

    dynamic_form = DynamicForm.objects.first()
    field_data = request.data.copy()
    field_data['dynamicform'] = dynamic_form.id
    formfield_serializer = FormFieldSerializer(data=field_data)

    if formfield_serializer.is_valid():
        formfield_serializer.save()
        messages.success(request, "Successfully added a new field!")
        return redirect('/viewfield')
    else:
        return Response(formfield_serializer.errors, status=400)

@login_required
@api_view(['DELETE'])
def deleteField(request, fieldID):
    try:
        deletingOBJ = FormField.objects.get(id=fieldID)
        deletingOBJ.delete()
        messages.success(request, "Successfully deleted a field!")
    except FormField.DoesNotExist:
        messages.error(request, "Field not found.")
    return redirect('/viewfield')

@login_required
@api_view(['POST'])
def addEmployee(request):
    dynamic_form = DynamicForm.objects.first()
    employeeOBJ = Employee.objects.create(dynamicform=dynamic_form)
    employeeOBJ.save()

    employee_data = request.data.copy()
    employee_data.pop("csrfmiddlewaretoken", None)
    for field_name, field_value in employee_data.items():
        try:
            form_field = FormField.objects.get(form_field=field_name)
            field_value_data = {
                "employee": employeeOBJ.id,
                "field": form_field.id,
                "value": field_value
            }
            field_value_serializer = FormFieldValueSerializer(data=field_value_data)
            if field_value_serializer.is_valid():
                field_value_serializer.save()
            else:
                return Response(field_value_serializer.errors, status=400)

        except FormField.DoesNotExist:
            return Response({"error": f"Field '{field_name}' does not exist."}, status=400)

    messages.success(request, "Successfully added employee details!")
    return redirect('/home')

@login_required
@api_view(['DELETE'])
def deleteEmployee(request, empID):
    try:
        deletingOBJ = Employee.objects.get(id=empID)
        deletingOBJ.delete()
        messages.success(request, "Successfully deleted an employee record!")
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found.")
    return redirect('/home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            Admin.objects.get(admin_name=username)
            try:
                request.session['user_id'] = Admin.objects.get(admin_name=username, admin_password=password).id
                messages.success(request, f"Welcome, {username}!")
                return redirect('/home')  
            except:
                messages.error(request, "Invalid password. Please try again.")
        except Admin.DoesNotExist:
            messages.error(request, "User does not exist. Please register first.")
    return redirect("/") 

@login_required
def logout_view(request):
        del request.session['user_id']
        return redirect('/')

def register_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Admin.objects.filter(admin_email=email).exists():
            messages.error(request, "Email already registered. Please login.")
            return redirect('/login')  
        admin = Admin(
            admin_name=fullname,
            admin_email=email,
            admin_password=password
        )
        admin.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect('/')  
    return render(request, 'login_reg.html')  

