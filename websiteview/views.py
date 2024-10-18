from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        print("sucses")
        #return reverse('index')


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
    return render(request, 'index.html')  # Path to your index template
