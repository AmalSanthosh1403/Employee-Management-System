from rest_framework import serializers
from .models import DynamicForm, FormField, Employee, FormFieldValue

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'form_field', 'field_type', 'dynamicform']

    def create(self, validated_data):
        new_field = FormField.objects.create(**validated_data)

        employees = Employee.objects.all()
        for employee in employees:
            FormFieldValue.objects.create(
                field=new_field,
                employee=employee,
                value="Details not provided"
            )

        return new_field

class DynamicFormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True,  read_only=True)
    class Meta:
        model = DynamicForm
        fields = ['id', 'dynamicform_name', 'fields']

    
class FormFieldValueSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.form_field', read_only=True)

    class Meta:
        model = FormFieldValue
        fields = ['id', 'field', 'field_name', 'value', 'employee']
class EmployeeSerializer(serializers.ModelSerializer):
    field_values = FormFieldValueSerializer(many=True, read_only=True)  

    class Meta:
        model = Employee
        fields = ['id', 'dynamicform', 'field_values']

    
