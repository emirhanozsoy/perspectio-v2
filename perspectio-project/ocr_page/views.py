from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import ast
import json
import time
import random
import sqlite3
import requests
from PIL import Image
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

def detect_text(path):
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print('Texts:')

    for text in texts:
        return text.description
        break

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def detect_handwriting(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    words = ""
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    words = words+word_text + ' '
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    return words


def get_filename(extension):
    file_name = ''
    for a in range(30):
        file_name += random.choice(characters)

    new_file = file_name+"."+extension
    return new_file

# Create your views here.
def ocr_page(request):
    print(request.POST)
    uploaded_file_urls=[]
    if request.method == 'POST' and 'myFile' in request.FILES and request.POST.get("uploadbtn"):
        
        myfile= request.FILES
        for file in myfile.getlist('myFile'):
            fs = FileSystemStorage()
            filename = fs.save(get_filename('jpg'), file)
            uploaded_file_urls.append(fs.url(filename))

        return render(request, 'ocr_page/ocr_page.html', {'uploaded_file_urls': uploaded_file_urls})
    
    if request.method == 'POST' and request.POST.get("ocrbtn") and request.POST.get("handwriting"):
        ocr=''
        liste=list(request.POST.get("ocrbtn").replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(","))
        print(liste)
        for i in liste:
            pat=i[1:]
            print(pat)
            result=detect_handwriting(pat)
            ocr=ocr+result

        return render(request, 'ocr_page/ocr_page.html', {'uploaded_file_urls': liste,'ocr':ocr})

    if request.method == 'POST' and request.POST.get("ocrbtn"):
        print(request.POST)
        ocr=''
        liste=list(request.POST.get("ocrbtn").replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(","))
        print(liste)
        for i in liste:
            pat=i[1:]
            print(pat)
            result=detect_text(pat)
            ocr=ocr+result

        return render(request, 'ocr_page/ocr_page.html', {'uploaded_file_urls': liste,'ocr':ocr})
    
    

    return render(request,'ocr_page/ocr_page.html')