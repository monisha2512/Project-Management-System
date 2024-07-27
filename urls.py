"""
URL configuration for first project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from ap1 import views
from ap1.views import createproject, date, login,eventschedule, layout,home, loginpage, progress, report,synopsis, index,projectadmin,createteam, register, regstudent, reportupload, schedule, table_created, teamcreation, uploadreport, uploadsyn, uploadsynopsis, viewprojectstatus, viewprojectteam, viewschedule, viewstudentlist, viewteam, weeklyprogress, weeklyreport,logout
from first import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('layout/',layout),
    path('login/',login),
    path('register/',register),
    path('teamcreation/',teamcreation),
    path('uploadsynopsis/',uploadsyn),
    path('reportupload/',uploadreport),
    path('viewprojectstatus/',viewprojectstatus),
    path('weeklyreport/',weeklyreport),
    path('home/',home),
    path('weeklyprogress/',weeklyprogress),
    path('viewschedule/',viewschedule),
    path('viewteam/',viewteam),
    path('viewstudentlist/',viewstudentlist),
    path('viewprojectteam/',viewprojectteam),
    path('schedule/',schedule),
    path('index/',index),
    path('projectadmin/',projectadmin),
    path('regstudent/',regstudent),
    path('createteam/',createteam),
    path('createproject/',createproject),
    path('synopsis/',synopsis),
    path('progress/',progress),
    path('report/',report),
    path('eventschedule/',eventschedule),
    path('loginpage/',loginpage),
    path('logout/',logout),
    path('table_created/',table_created),
    path('viewstudentlist/', views.studentlist, name='studentlist'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL_1,
                          document_root=settings.MEDIA_ROOT_1)