from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import Enginer.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Enginer.views.home),
    path('demand/', Enginer.views.demand),
    path('geography/', Enginer.views.geography),
    path('skills/', Enginer.views.skills)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
