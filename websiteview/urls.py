from django.urls import path
from .views import loginpage,index,logoutpage

urlpatterns = [
    path('login/', loginpage, name='login'),
    path('', index, name='index'),
    path('logout/',logoutpage,name="logout")
]
