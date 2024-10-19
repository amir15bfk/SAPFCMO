from django.urls import path
from .views import receive_machine_data
from .views import SendMachineDataView , chart_data, get_machine_data, get_machine_data20E

urlpatterns = [
    path('receive-machine-data/<str:machine_id>/', receive_machine_data, name='receive_machine_data'),
    path('send-machine-data/', SendMachineDataView.as_view(), name='send_machine_data'),
    path('chart_data/', chart_data, name='chart_data'),
    path('get_machine_data/<str:machine_id>/', get_machine_data, name='get_machine_data'),
    path('get_machine_data20e/<str:machine_id>/', get_machine_data20E, name='get_machine_data'),
]