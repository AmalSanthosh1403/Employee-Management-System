from django.db import models

class Admin(models.Model):
    admin_name = models.CharField(max_length=100)
    admin_email = models.EmailField(unique=True)
    admin_password = models.CharField(max_length=50)

    def __str__(self):
        return self.admin_name


# form models
class DynamicForm(models.Model):
    dynamicform_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dynamicform_name


class FormField(models.Model):
    FIELD_TYPES = [
        ('Text', 'Text'),
        ('Number', 'Number'),
        ('Date', 'Date'),
        ('Password', 'Password'),
    ]

    dynamicform = models.ForeignKey(DynamicForm, on_delete=models.CASCADE, related_name="fields")
    form_field = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)

    def __str__(self):
        return f"{self.form_field} ({self.field_type})"
    
class Employee(models.Model):
    dynamicform = models.ForeignKey(DynamicForm, on_delete=models.CASCADE, related_name="employees")

    def __str__(self):
        return f"Employee {self.id} ({self.dynamicform.dynamicform_name})"


class FormFieldValue(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="field_values")
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f"{self.field.form_field}: {self.value}"


    
