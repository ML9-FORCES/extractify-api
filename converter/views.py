from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from pdf2image import convert_from_path
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
def pdftoimg(request):
    if(request.method == "POST"):
        pdf = request.FILES['pdf_name']
        with open('./converter/tempfiles/temp.pdf', 'wb+') as destination:
            for chunk in pdf.chunks():
                destination.write(chunk)
        images = convert_from_path('./converter/tempfiles/temp.pdf')
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save('./converter/tempfiles/temp' +
                           str(i) + '.jpg', 'JPEG')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'})
