from django.urls import path, include
from converter.views import pdftoimg

urlpatterns = [
    path('pdftoimg/', pdftoimg)
]
