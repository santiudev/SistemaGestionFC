from django.shortcuts import render

def error_403_view(request, exception):
    return render(request, 'errors/error403.html', status=403)