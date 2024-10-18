from django.urls import path
from .views import receive_machine_data
from .views import SendMachineDataView

urlpatterns = [
    path('receive-machine-data/<str:machine_id>/', receive_machine_data, name='receive_machine_data'),
    path('send-machine-data/', SendMachineDataView.as_view(), name='send_machine_data')
]