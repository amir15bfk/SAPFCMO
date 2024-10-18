from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from webhook_handler.models import Machine

from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def loginpage(request):
    print('chakib')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        
        user = authenticate(request, username=username, password=password)  # Authenticate the user
        print(user)
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
    print(user_groups)



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


