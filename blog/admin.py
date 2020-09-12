# bizim oluşturudugumuz modelin admin sayfasında görünmesini saglıyor.
# 
from django.contrib import admin
from .models import *

admin.site.register(Blog)
admin.site.register(Kategori)
admin.site.register(Comment)


