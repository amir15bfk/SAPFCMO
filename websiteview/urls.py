from django.urls import path
from .views import loginpage,index

urlpatterns = [
    path('login/', loginpage, name='login'),
    path('', index, name='index'),
]
