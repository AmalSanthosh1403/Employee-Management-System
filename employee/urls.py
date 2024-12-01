from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_regFuntion, name='login_reg'), 
    path('login', views.login_view, name='login'),  
    path('register', views.register_view, name='register'),  
    path('logout', views.logout_view, name='logout'),  
    path('home', views.homePage, name='homepage'),  
    path('viewfield', views.formFields, name='view_field'),  
    path('addfield', views.addField, name='add_field'),
    path('deletefield/<int:fieldID>', views.deleteField, name='delete_field'),
    path('addemployee', views.addEmployee, name='add_employee'),
    path('deleteemployee/<int:empID>', views.deleteEmployee, name='delete_employee'),


]
