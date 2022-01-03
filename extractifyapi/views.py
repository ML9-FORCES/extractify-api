# HttpResponse is used to
# pass the information
# back to view
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Defining a function which
# will receive request and
# perform task depending
# upon function definition


def ping(request):
    return HttpResponse("Pong")
