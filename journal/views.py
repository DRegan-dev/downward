from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    """
        Homepage view for Downward
        Acessible to all users
    """

    return render(request, 'journal/home.html')