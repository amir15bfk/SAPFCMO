from django.urls import path
from .views import loginpage,index,logoutpage,product_detail,maitenance_page,send_notification_email

urlpatterns = [
    path('login/', loginpage, name='login'),
    path('', index, name='index'),
    path('logout/',logoutpage,name="logout"),
    path('product/<str:machines_id>/', product_detail, name='product_detail'),
    path('maintenance/', maitenance_page, name='maitenance_page'),
    path('sendemail/', send_notification_email, name='send_notification_email')
]
