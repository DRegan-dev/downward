from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

# Create your views here.

def register(request):
    if request.methoD == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Accuont created Sucessfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')