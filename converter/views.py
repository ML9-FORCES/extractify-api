from django.http.response import HttpResponse
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
        pdf = request.data
        images = convert_from_path(pdf)
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save('page' + str(i) + '.jpg', 'JPEG')
        return Response({'key': request.data}, status=status.HTTP_200_OK)

    # except:
    #     Result = "NO pdf found"
    #     ("Result", Result)

    # else:
    #     Result = "success"
    #     messagebox.showinfo("Result", Result)
