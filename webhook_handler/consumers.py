from channels.generic.websocket import AsyncWebsocketConsumer
import json
from webhook_handler.models import Machine
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder

connected_clients = set()
class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected")
        connected_clients.add(self)
        await self.accept()

    async def disconnect(self, close_code):
        if self in connected_clients:
            connected_clients.remove(self)
        print(f'WebSocket connection closed with code: {close_code}')

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            machine_id = text_data_json.get('machine_id')

            if not machine_id:
                await self.send_error("Missing machine_id in the request")
                return

            response = await self.get_machine_data(machine_id)

            if response:
                await self.send(text_data=json.dumps({
                    'machine': machine_id,
                    'response': response
                }, cls=DjangoJSONEncoder))
            else:
                await self.send_error(f"No data found for machine_id: {machine_id}")

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format in the request")
        except Exception as e:
            await self.send_error(f"An error occurred: {str(e)}")

    @database_sync_to_async
    def get_machine_data(self, machine_id):
        machine = Machine.objects.filter(machine_id=machine_id).first()
        if machine:
            sensor_data = machine.sensor_data.order_by('-timestamp').first()
            if sensor_data:
                return {
                    'timestamp': sensor_data.timestamp,
                    'data': sensor_data.data
                }
        return None

    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'error': message
        }))

    async def send_anomaly_message(self, message):
        await self.send(text_data=json.dumps({
            'message': message
        }))
async def notify_all_clients_anomaly(message):
    print(1)
    for client in connected_clients:
        print(1)
        await client.send_anomaly_message(message)