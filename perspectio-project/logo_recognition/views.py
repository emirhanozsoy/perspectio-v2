from django.shortcuts import render

# Create your views here.
def logo_recognition(request):

    return render(request,'logo_recognition/logo_recognition.html')