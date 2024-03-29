from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import ast
import json
import time
import random
import sqlite3
import requests
from PIL import Image, ImageDraw
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


def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    return faces
    # for face in faces:
    #     print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
    #     print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
    #     print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                  for vertex in face.bounding_poly.vertices])

    #     return face.bounding_poly

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def get_filename(extension):
    file_name = ''
    for a in range(30):
        file_name += random.choice(characters)

    new_file = file_name+"."+extension
    return new_file

# Create your views here.


def face_recognition(request):
    return_dict={}
    # print(request.POST)
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

        return render(request, 'face_recognition/face_recognition.html',return_dict)

    if request.method == 'POST' and request.POST.get("recognize"):
      
        liste = list(request.POST.get("recognize").replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(","))
        try:
            for i in liste:
                faces = detect_faces(str(i[1:]))
                if faces:
                    for face in faces:
                        image = Image.open(i[1:])
                        rgb_im = image.convert('RGB')
                        draw = ImageDraw.Draw(image)
                        draw.rectangle(((face.bounding_poly.vertices[0].x, face.bounding_poly.vertices[0].y), (
                            face.bounding_poly.vertices[2].x, face.bounding_poly.vertices[2].y)), outline="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]),  width=5)
                        image.save(i[1:])
                    return_dict= {'uploaded_file_urls': liste}
                else:
                    noface=1
                    return_dict= {'uploaded_file_urls': liste,'noface':noface}

            
        except:
            error2=1
            return_dict= {'error2': error2}

        return render(request, 'face_recognition/face_recognition.html',return_dict)

    return render(request, 'face_recognition/face_recognition.html')
