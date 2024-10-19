from django.urls import path
from .views import loginpage,index,logoutpage,product_detail

urlpatterns = [
    path('login/', loginpage, name='login'),
    path('', index, name='index'),
    path('logout/',logoutpage,name="logout"),
    path('product/<str:machines_id>/', product_detail, name='product_detail'),
]
