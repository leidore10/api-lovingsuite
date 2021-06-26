from django.conf import settings
from django.conf.urls import *

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.urls import path
from home.views import *
from api.views import *
from apps.utils import UtilClass
from api.public.views import *
from apps.core.views import *
from rest_framework.authtoken import views

admin.autodiscover()

urlpatterns = [
				# User management
                path('', index, name='index'),
                path('admin/', admin.site.urls),
                path('admin/doc/', include('django.contrib.admindocs.urls')),
                path('app/', include('apps.urls')),
                path('api/v1.0/', include(('api.urls', 'api'))),
                path('api/v1.0/auth/login/', UserAuthToken.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
