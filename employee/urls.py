from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_regFuntion, name='login_reg'),  
    path('home', views.homePage, name='homepage'),  
    path('viewfield', views.formFields, name='view_field'),  
    path('addfield', views.addField, name='add_field'),
    path('deletefield/<int:fieldID>', views.deleteField, name='delete_field'),

]
