from django.shortcuts import render

# Create your views here.
def landmark_recognition(request):

    return render(request, 'landmark_recognition/landmark_recognition.html')