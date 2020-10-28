from django.contrib import admin
from django.urls import path
from homepage.views import homepage
from ocr_page.views import ocr_page
from face_recognition.views import face_recognition
from landmark_recognition.views import landmark_recognition
from logo_recognition.views import logo_recognition

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="homepage"),
    path('ocr/', ocr_page, name="ocr_page"),
    path('face_recognition/', face_recognition, name="face_recognition"),
    path('landmark_recognition/', landmark_recognition, name="landmark_recognition"),
    path('logo_recognition/', logo_recognition, name="logo_recognition"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)