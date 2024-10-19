
# SAPFCMO Project

- by **Ariane09+ team**

## Requirements

- Python 3.x
- Django
- pip (Python package manager)
- ngrok
- An SMTP mail service for sending emails (e.g., Gmail API, SendGrid)

## Setup

### 1. Install Project Dependencies

First, clone the project repository and navigate to the project directory:

```bash
git clone https://github.com/amir15bfk/SAPFCMO.git
cd SAPFCMO
```

Now, install the required Python packages by running:

```bash
pip install -r requirements.txt
```

### 2. Running Migrations

To set up the database, apply the Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Configure Ngrok for Webhooks

The project requires an external tunnel service to expose the local Django server to the internet. Ngrok is used for this purpose.

#### 3.1 Install ngrok

You can download ngrok from the official website: https://ngrok.com/download

After downloading, run ngrok by specifying the port your Django app will run on (default is `8000`):

```bash
./ngrok http 8000
```

This will generate a public URL like `https://<ngrok-id>.ngrok.io`. Copy this URL for the next steps.

#### 3.2 Update Webhook Handler

In the file `webhook_handler/management/commands/send_machine_data.py`, update the webhook URL with the ngrok URL generated in the previous step.

Replace the placeholder URL in the script with your actual ngrok link:

```python
WEBHOOK_URL = "https://<ngrok-id>.ngrok.io/webhook-endpoint"
```

#### 3.3 Add Ngrok URL to Allowed Hosts

To ensure Django allows requests from the ngrok URL, open the `settings.py` file located in the `SAPFCMO/` directory and add the ngrok URL to the `ALLOWED_HOSTS` list:

```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '<ngrok-id>.ngrok.io']
```

### 4. Configure Mail API

The project sends notifications through emails. Configure your mail service (e.g., Gmail, SendGrid) in the `settings.py` file:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

Alternatively, you can use an environment variable to store sensitive information.

### 5. Start the Development Server

Now you can start the Django development server:

```bash
python manage.py runserver
```

### 6. Subscribe to the Webhook

Once your server is running and ngrok is exposing it, subscribe to the webhook using the following command:

```bash
python manage.py send_machine_data --all
```

This command will trigger the process that sends data from all machines and ensures the webhook subscriptions are active.

## Additional Commands

- To view available management commands, run:

  ```bash
  python manage.py help
  ```

- For detailed logging and debugging of webhook data being sent, check the Django console output or logs.

## Troubleshooting

- If you encounter errors related to the webhook, verify that ngrok is running and the webhook URL in `send_machine_data.py` is correct.
- Ensure that the Django server is reachable via the ngrok URL and is not blocked by firewalls.
- If emails are not sending, check your SMTP configuration and ensure that less secure apps are enabled if using Gmail.

## License

This project is licensed under the MIT License.