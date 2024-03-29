from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import ast
import json
import time
import random
import sqlite3
import requests
from PIL import Image, ImageDraw,ImageFont
from docx import Document
from docx.shared import Inches
from sqlite3 import Error
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect, csrf_exempt


characters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower())
characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
characters.extend(list('0123456789'))

def get_filename(extension):
    file_name = ''
    for a in range(30):
        file_name += random.choice(characters)

    new_file = file_name+"."+extension
    return new_file

def detect_logos(path):
    """Detects logos in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return logos

# Create your views here.
def logo_recognition(request):

    return_dict={}
    uploaded_file_urls = []

    if request.method == 'POST' and 'myFile' in request.FILES and request.POST.get("uploadbtn"):
        try:
            myfile = request.FILES
            for file in myfile.getlist('myFile'):
                fs = FileSystemStorage()
                filename = fs.save(get_filename('jpg'), file)
                uploaded_file_urls.append(fs.url(filename))

            return_dict= {'uploaded_file_urls': uploaded_file_urls}
        except:
            error2=1
            return_dict= {'error2': error2}


        return render(request, 'logo_recognition/logo_recognition.html', return_dict)
    
    if request.method == 'POST' and request.POST.get("recognize"):

        liste = list(request.POST.get("recognize").replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(","))
        try:

            for i in liste:
                logos = detect_logos(str(i[1:]))
                if logos:
                    for logo in logos:
                        image = Image.open(i[1:])
                        rgb_im = image.convert('RGB')
                        draw = ImageDraw.Draw(image)
                        color="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                        font_type = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28, encoding="unic")
                        draw.text((logo.bounding_poly.vertices[0].x+10,logo.bounding_poly.vertices[0].y-30), logo.description, font=font_type, fill=color)
                        draw.rectangle(((logo.bounding_poly.vertices[0].x, logo.bounding_poly.vertices[0].y), (
                            logo.bounding_poly.vertices[2].x, logo.bounding_poly.vertices[2].y)), outline=color,  width=5)

                        image.save(i[1:])
                    return_dict={'uploaded_file_urls': liste}
                else:
                    nologo=1
                    return_dict= {'uploaded_file_urls': liste,'nologo':nologo}
        except:
            error2=1
            return_dict= {'error2': error2}

        return render(request, 'logo_recognition/logo_recognition.html', return_dict)

    return render(request,'logo_recognition/logo_recognition.html')