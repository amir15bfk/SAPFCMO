

# # Create your views here.
# # webhook_handler/views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.dateparse import parse_datetime
# from .models import MachineData
# import json

# @csrf_exempt
# def receive_machine_data(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)

#         # Parse the data from the request
#         machine_id = data.get('machine_id')
#         timestamp = parse_datetime(data.get('timestamp'))
#         weld_temperature = data.get('weld_temperature')
#         weld_current = data.get('weld_current')
#         weld_voltage = data.get('weld_voltage')
#         weld_time = data.get('weld_time')
#         pressure_applied = data.get('pressure_applied')
#         arm_position = data.get('arm_position', {})
#         arm_position_x = arm_position.get('x')
#         arm_position_y = arm_position.get('y')
#         arm_position_z = arm_position.get('z')
#         wire_feed_rate = data.get('wire_feed_rate')
#         gas_flow_rate = data.get('gas_flow_rate')
#         weld_strength_estimate = data.get('weld_strength_estimate')
#         vibration_level = data.get('vibration_level')
#         power_consumption = data.get('power_consumption')

#         # Save the data to the database
#         MachineData.objects.create(
#             machine_id=machine_id,
#             timestamp=timestamp,
#             weld_temperature=weld_temperature,
#             weld_current=weld_current,
#             weld_voltage=weld_voltage,
#             weld_time=weld_time,
#             pressure_applied=pressure_applied,
#             arm_position_x=arm_position_x,
#             arm_position_y=arm_position_y,
#             arm_position_z=arm_position_z,
#             wire_feed_rate=wire_feed_rate,
#             gas_flow_rate=gas_flow_rate,
#             weld_strength_estimate=weld_strength_estimate,
#             vibration_level=vibration_level,
#             power_consumption=power_consumption
#         )

#         return JsonResponse({'status': 'success'})

#     return JsonResponse({'status': 'invalid method'}, status=405)

# import requests
# from django.http import JsonResponse
# from django.views import View

# class SendMachineDataView(View):
#     def post(self, request, *args, **kwargs):
#         url = "https://manufcaturing-challenge-production.up.railway.app/Webhook"
#         payload = {
#             "machine": "welding_robot_006",
#             "callback_url": "https://90d2-41-105-223-87.ngrok-free.app/webhook/receive-machine-data/"
#         }
#         response = requests.post(url, json=payload)

#         return JsonResponse(response.json(), safe=False)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Machine, SensorData, LatestSensorData
import json
import requests

@csrf_exempt
def receive_machine_data(request, machine_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Retrieve the Machine instance
        machine = get_object_or_404(Machine, machine_id=machine_id)

        timestamp = parse_datetime(data.get('timestamp'))

        # Prepare sensor data
        
        sensor_data = {key: data.get(key) for key in data.keys() if key != 'timestamp'}


        # Save to SensorData
        SensorData.objects.create(
            machine=machine,
            timestamp=timestamp,
            data=sensor_data
        )

        # Update or create LatestSensorData
        LatestSensorData.objects.update_or_create(
            machine=machine,
            defaults={
                'timestamp': timestamp,
                'data': sensor_data
            }
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'invalid method'}, status=405)

class SendMachineDataView(View):
    def post(self, request, *args, **kwargs):
        machine_id = request.POST.get('machine_id')
        print(request)
        machine = get_object_or_404(Machine, machine_id=machine_id)

        url = "https://manufcaturing-challenge-production.up.railway.app/Webhook"
        payload = {
            "machine": machine.machine_id,
            "callback_url": machine.webhook_url
        }
        response = requests.post(url, json=payload)

        return JsonResponse(response.json(), safe=False)