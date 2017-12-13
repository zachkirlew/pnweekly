from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^', include('users.urls')),
                  url(r'^', include('articles.urls')),
              ]+static(settings.MEDIA_ROOT, document_root=settings.MEDIA_URL)
