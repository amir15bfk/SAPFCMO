from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = "Send machine data to an external server."

    def handle(self, *args, **kwargs):
        url = "https://manufcaturing-challenge-production.up.railway.app/Webhook"
        payload = {
            "machine": "welding_robot_006",
            "callback_url": "https://90d2-41-105-223-87.ngrok-free.app/webhook/receive-machine-data/"
        }
        response = requests.post(url, json=payload)

        self.stdout.write(self.style.SUCCESS(f"Response: {response.json()}"))
