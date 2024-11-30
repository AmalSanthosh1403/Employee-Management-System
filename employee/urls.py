from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_regFuntion, name='login_reg'),  # This is valid
]
