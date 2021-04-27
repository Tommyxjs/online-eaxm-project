from django.contrib import admin
from django.urls import path, include

from stuapp import views
from questionsapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stu/', include('stuapp.urls')),
    path('questions/', include('questionsapp.urls'))
]