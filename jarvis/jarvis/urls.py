from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('diet/', include('diet.urls')),
    path('admin/', admin.site.urls),
]
