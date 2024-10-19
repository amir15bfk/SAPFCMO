

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
from webhook_handler import process_sensor_data
from webhook_handler.anomaly_detection import *
from webhook_handler.anomalyutils import *
from webhook_handler.consumers import *
from asgiref.sync import async_to_sync


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
        flattened_data = process_new_data_point(sensor_data,machine)
        output = detect_anomaly_for_point(flattened_data, machine.machine_type)
        if output["is_general_anomaly"]:
            # Send an email alert
            # send_anomaly_alert(machine, output)

            # # Create a task
            # create_task(machine, output)

            # Notify via WebSockets
            message = f"Anomaly detected in {machine.name}. Details: {output}"
            async_to_sync(notify_all_clients_anomaly)(message)

            print('Anomaly detected!')

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


def  chart_data(request, machine_id):
    machine = get_object_or_404(Machine, machine_id=machine_id)
    latest_data = LatestSensorData.objects.filter(machine=machine).first()
    if latest_data:
        return JsonResponse(latest_data.data, safe=False)
    else:
        return JsonResponse({}, safe=False)



def chart_data(request):
    machine = [{"machine_id": machine.machine_id, "power_consumption": machine.latest_data.data.get('power_consumption')} 
               for machine in Machine.objects.all() if machine.latest_data.data.get('power_consumption')]
    return JsonResponse(machine, safe=False)

def get_machine_data(request, machine_id):
    machine = Machine.objects.filter(machine_id=machine_id).first()
    if machine and machine.sensor_data.exists():
        latest_data = machine.sensor_data.order_by('-timestamp').first().data
        return JsonResponse(latest_data, safe=False)
    else:
        return JsonResponse({}, safe=False)

def get_machine_data20E(request, machine_id):
    machine = Machine.objects.filter(machine_id=machine_id).first()
    if machine and machine.sensor_data.exists():
        latest_data = machine.sensor_data.order_by('-timestamp')[:20]
        dic = {"label": "", "data": []}

        # Check what data type the machine provides
        if latest_data.first().data.get('power_consumption'):
            dic["label"] = "Power Consumption"
            dic["data"] = [d.data.get('power_consumption') for d in latest_data]
        elif latest_data.first().data.get('paint_thickness'):
            dic["label"] = "Paint Thickness"
            dic["data"] = [d.data.get('paint_thickness') for d in latest_data]
        elif latest_data.first().data.get('leak_rate'):
            dic["label"] = "Leak Rate"
            dic["data"] = [d.data.get('leak_rate') for d in latest_data]
        elif latest_data.first().data.get('battery_level'):
            dic["label"] = "Battery Level"
            dic["data"] = [d.data.get('battery_level') for d in latest_data]
        
        return JsonResponse(dic, safe=False)
    else:
        return JsonResponse({}, safe=False)
