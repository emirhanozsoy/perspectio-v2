from django.contrib import admin
from django.urls import path
from homepage.views import homepage
from ocr_page.views import ocr_page
from face_recognition.views import face_recognition
from landmark_recognition.views import landmark_recognition
from logo_recognition.views import logo_recognition
from perspectio.sitemaps import Static_Sitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

sitemaps = {
    'static': Static_Sitemap(),
}

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', homepage, name="homepage"),
    path('ocr/', ocr_page, name="ocr_page"),
    path('facerecognition/', face_recognition, name="face_recognition"),
    path('landmarkrecognition/', landmark_recognition, name="landmark_recognition"),
    path('logorecognition/', logo_recognition, name="logo_recognition"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)