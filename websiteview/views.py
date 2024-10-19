from datetime import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from webhook_handler.models import Machine,SensorData,MaintenanceProfile,Task

from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .decoratr import group_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)  # Authenticate the user
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('index')  # Redirect to the index page
        else:
            error = "Invalid username or password"  # Set an error message if authentication fails
            return render(request, "login.html", {"error": error})  # Render the template with error message

    return render(request, "login.html")  # Render the template for GET requests






@login_required
def index(request):
    machines=Machine.objects.all()
    user_groups = request.user.groups.values_list('name', flat=True)



    context = {
        'user': request.user,
        'machines':machines,
        'user_groups':user_groups
    }
    return render(request, 'index.html',context)  # Path to your index template*

@login_required
def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required
def product_detail(request, machines_id):
    machines=Machine.objects.all()
    user_groups = request.user.groups.values_list('name', flat=True)


    machine = Machine.objects.get(machine_id=machines_id)
    sensor_data = SensorData.objects.filter(machine=machine).order_by('-timestamp')
    try:
        data=sensor_data.first().data.keys()
    except:
        data={}




    context = {
        "machine_id": machine.machine_id,
        'user': request.user,
        'machines':machines,
        'user_groups':user_groups,
        'sensor_data':sensor_data,
        'datas':data
    }
    return render(request, 'machine.html',context)

@login_required
@group_required('maitenance')
def maitenance_page(request):
    machines=Machine.objects.all()
    user_groups = request.user.groups.values_list('name', flat=True)
    if request.user.groups.filter(name="manager").exists():
        tasks=Task.objects.all()
    else:
        
        user=MaintenanceProfile.objects.filter(user=request.user).first()
        tasks=Task.objects.filter(taskdoneby=user)





    context = {
        'user': request.user,
        'machines':machines,
        'user_groups':user_groups,
        'tasks':tasks,
    }
    return render(request, 'maintenance.html',context)



from django.core.mail import send_mail
from django.http import HttpResponse


@login_required
def send_notification_email(request):
    
    subject = 'Machine Issue Notification'
    message = 'A new issue has been detected in Machine #3.'
    from_email = 'chakib.aitsaada@gmail.com'
    recipient_list = ['tchako12356@gmail.com']  # List of recipients


    result=send_mail(subject, message, from_email, recipient_list,fail_silently=False)
    return HttpResponse(str(result))


@login_required
@require_http_methods(["POST"])
def update_task(request):
    random_profile = MaintenanceProfile.objects.order_by('?').first()
    try:
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        
        # Update completion status if provided
        if 'completed' in request.POST:
            completed = request.POST.get('completed') == 'true'
        
        # Update report if provided
        if 'report' in request.POST:
            task.report = request.POST.get('report')
                                           
        task.completed=True
        
        task.save()

        if not completed:
            new_task = Task(
            title=task.title,
            description=task.description+" "+task.report,
            completed=False,
            report="",
            type=task.type,
            machine=task.machine,
            taskdoneby=random_profile
            )
            new_task.save()
        return JsonResponse({'status': 'success'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from webhook_handler.models import Machine
from anomaly_forcasting import load_and_preprocess_data, forecast_machine_data

@login_required
def forecast_page(request):
    machines = Machine.objects.all()
    forecast_data = {}

    for machine in machines:
        machine_type = machine.machine_type
        user_groups = request.user.groups.values_list('name', flat=True)
        df = load_and_preprocess_data(machine_type)
        
        forecast_data[machine_type] = {}
        numerical_columns = df.select_dtypes(include=['number']).columns
        for column in numerical_columns:
            forecast, forecast_index = forecast_machine_data(machine_type, column)
            forecast_data[machine_type][column] = {
                'forecast': forecast.tolist(),
                'forecast_index': forecast_index.strftime('%m-%d %H').tolist()
            }
    print(forecast_data)
    context = {
        'forecast_data': forecast_data,
        'machines': machines,
        'user_groups':user_groups,
        'user': request.user
    }
    return render(request, 'forecast.html', context)







