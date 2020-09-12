from django.contrib import admin
from django.urls import path, include
from blog.views import *
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from blog.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('blog.urls')),
    path('auths/', include('auths.urls')),
    path('iletisim/', iletisim, name='iletisim'),

]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
