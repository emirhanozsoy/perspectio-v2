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

def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')
    
    for landmark in landmarks:
        # print(landmark)
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return(landmarks)


# Create your views here.
def landmark_recognition(request):

    print(request.POST)
    uploaded_file_urls = []
    if request.method == 'POST' and 'myFile' in request.FILES and request.POST.get("uploadbtn"):

        myfile = request.FILES
        for file in myfile.getlist('myFile'):
            fs = FileSystemStorage()
            filename = fs.save(get_filename('jpg'), file)
            uploaded_file_urls.append(fs.url(filename))

        return render(request, 'landmark_recognition/landmark_recognition.html', {'uploaded_file_urls': uploaded_file_urls})

    if request.method == 'POST' and request.POST.get("recognize"):
        print(request.POST)
        ocr = ''
        landmarks_names=[]
        liste = list(request.POST.get("recognize").replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(","))
 
        for i in liste:
            landmarks = detect_landmarks(str(i[1:]))
            if landmarks:
                for landmark in landmarks:
                    if landmark.description not in landmarks_names:
                        print(landmark.description)
                        print(landmark)
                        color="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                        image = Image.open(i[1:])
                        rgb_im = image.convert('RGB')
                        draw = ImageDraw.Draw(image)
                        draw.rectangle(((landmark.bounding_poly.vertices[0].x, landmark.bounding_poly.vertices[0].y), (landmark.bounding_poly.vertices[2].x, landmark.bounding_poly.vertices[2].y)), outline=color,  width=5)
                        draw.text((landmark.bounding_poly.vertices[0].x+10,landmark.bounding_poly.vertices[0].y+10), landmark.description, font=ImageFont.truetype("arial",14), fill=color)
                        landmarks_names.append(landmark.description)
                        image.save(i[1:])
                        for location in landmark.locations:
                            lat_lng = location.lat_lng
                            latitude=lat_lng.latitude
                            longitude=lat_lng.longitude


        url="https://maps.google.com/maps?q="+str(latitude) +","+str(longitude) +"&output=embed"
        return render(request, 'landmark_recognition/landmark_recognition.html', {'uploaded_file_urls': liste,'latitude':latitude,'longitude':longitude,'url':url})

    return render(request, 'landmark_recognition/landmark_recognition.html')