from django.shortcuts import render

# Create your views here.
def face_recognition(request):

    return render(request,'face_recognition/face_recognition.html')