from rest_framework import serializers
from .models import DynamicForm, FormField, Employee, FormFieldValue

class FormFieldSerializer(serializers.ModelSerializer):
    """
    Handles individual form fields.
    """
    class Meta:
        model = FormField
        fields = ['id', 'form_field', 'field_type', 'dynamicform']

class DynamicFormSerializer(serializers.ModelSerializer):
    """
    Handles the serialization of DynamicForm, including nested FormField.
    """
    fields = FormFieldSerializer(many=True,  read_only=True)  # Include related FormField instances

    class Meta:
        model = DynamicForm
        fields = ['id', 'dynamicform_name', 'fields']

    
class FormFieldValueSerializer(serializers.ModelSerializer):
    """
    Handles individual form field values for an employee.
    """
    class Meta:
        model = FormFieldValue
        fields = ['id', 'field', 'value', 'employee']

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Handles Employee serialization with nested FormFieldValue.
    """
    field_values = FormFieldValueSerializer(many=True, read_only=True)  # Include related FormFieldValue instances

    class Meta:
        model = Employee
        fields = ['id', 'dynamicform', 'field_values']

    