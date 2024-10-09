from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def error_403_view(request, exception):
    return render(request, 'errors/error403.html', status=403)


@login_required
def home(request):
    return render(request, 'users/home.html')

