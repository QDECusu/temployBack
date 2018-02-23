from django.http import HttpResponse

def home(request):
    return HttpResponse("The home route works")

def login(request):
    return HttpResponse("The login route works")
