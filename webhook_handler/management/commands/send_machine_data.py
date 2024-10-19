# from django.core.management.base import BaseCommand
# import requests

# class Command(BaseCommand):
#     help = "Send machine data to an external server."

#     def handle(self, *args, **kwargs):
#         url = "https://manufcaturing-challenge-production.up.railway.app/Webhook"
#         payload = {
#             "machine": "welding_robot_006",
#             "callback_url": "https://90d2-41-105-223-87.ngrok-free.app/webhook/receive-machine-data/"
#         }
#         response = requests.post(url, json=payload)

#         self.stdout.write(self.style.SUCCESS(f"Response: {response.json()}"))
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import requests
from webhook_handler.models import Machine  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = "Subscribe machines to the manufacturing challenge webhook."

    def add_arguments(self, parser):
        parser.add_argument('--machine_id', type=str, help='ID of the machine to subscribe')
        parser.add_argument('--all', action='store_true', help='Subscribe all machines')

    def handle(self, *args, **options):
        base_url = "https://6300-105-103-163-68.ngrok-free.app"  # Your base URL
        webhook_url = "https://manufcaturing-challenge-production.up.railway.app/Webhook"

        if options['all']:
            machines = Machine.objects.all()
        elif options['machine_id']:
            try:
                machines = [Machine.objects.get(machine_id=options['machine_id'])]
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f"Machine with ID {options['machine_id']} not found."))
                return
        else:
            self.stdout.write(self.style.ERROR("Please specify --machine_id or use --all"))
            return

        for machine in machines:
            payload = {
                "machine": machine.machine_id,
                "callback_url": f"{base_url}/webhook/receive-machine-data/{machine.machine_id}/"
            }
            
            try:
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status()
                self.stdout.write(self.style.SUCCESS(f"Subscribed {machine.machine_id}: {response.json()}"))
                
                # Update the machine's webhook_url
                machine.webhook_url = payload['callback_url']
                machine.save()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Failed to subscribe {machine.machine_id}: {str(e)}"))