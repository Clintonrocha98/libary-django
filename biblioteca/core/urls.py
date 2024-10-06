from django.contrib import admin
from django.urls import include, path
from biblioteca.urls import urlpatterns as core_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_urls))
]
