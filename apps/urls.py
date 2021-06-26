from django.conf import settings
from django.conf.urls import *
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
                  path('core/', include(router.urls)),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
#def generalmention(request,user_id,net,body,typenoty,stream,format=None):