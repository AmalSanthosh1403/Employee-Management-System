from django.shortcuts import render, redirect
from .models import *
from . serializer import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages



def login_regFuntion(request):
    return render(request,'login_reg.html')

@api_view(['GET'])
def homePage(request):
    formfieldobjs = FormField.objects.all()
    allobjs = FormFieldSerializer(formfieldobjs,many=True)
    return render(request,'homepage.html',{'field_datas':allobjs.data})


@api_view(['GET'])
def formFields(request):
    formfieldobjs = FormField.objects.all()
    allobjs = FormFieldSerializer(formfieldobjs,many=True)
    return render(request,'custom_field.html',{'field_datas':allobjs.data})

@api_view(['POST'])
def addField(request):
    if not DynamicForm.objects.exists():
        DynamicForm.objects.create(dynamicform_name="new dynamic form")

    dynamic_form = DynamicForm.objects.first()

    field_data = request.data.copy()
    field_data['dynamicform'] = dynamic_form.id 

    formfield_serializer = FormFieldSerializer(data=field_data)
    if formfield_serializer.is_valid():
        formfield_serializer.save()
        messages.success(request, "successfully Added a New Field...!")
        return redirect('/viewfield')
    else:
        return Response(formfield_serializer.errors, status=400)

@api_view(['DELETE'])
def deleteField(request, fieldID):
    deletingOBJ = FormField.objects.get(id = fieldID)
    deletingOBJ.delete()
    messages.success(request, "successfully Deleted a Field...!")
    return redirect('/viewfield')
