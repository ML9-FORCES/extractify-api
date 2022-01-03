from django.shortcuts import render
from pdf2image import convert_from_path

# Create your views here.


def pdftoimg(request):
    pdf = request.GET.get('pdf_name')
    print(pdf)
    images = convert_from_path(pdf)
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('page' + str(i) + '.jpg', 'JPEG')

    # except:
    #     Result = "NO pdf found"
    #     ("Result", Result)

    # else:
    #     Result = "success"
    #     messagebox.showinfo("Result", Result)
