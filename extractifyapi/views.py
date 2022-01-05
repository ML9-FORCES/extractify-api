# HttpResponse is used to
# pass the information
# back to view
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
# Defining a function which
# will receive request and
# perform task depending
# upon function definition


def ping(request):
    return HttpResponse("Pong")


def output(request):
    file = open('./extractifyapi/output.json')
    data = json.load(file)
    return JsonResponse(data)
