"""SmartHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views

#url para cada estado solicitado

urlpatterns = [
    path('', views.index),
    path('estado_AC', views.estado_AC),
    path('estado_LS', views.estado_LS),
    path('estado_LC', views.estado_LC),
    path('estado_LD', views.estado_LD),
    path('estado_LB', views.estado_LB),
    path('estado_SM', views.estado_SM),
    path('estado_LDR', views.estado_LDR),
    path('estado_LDRon', views.estado_LDRon),
    path('estado_LDRoff', views.estado_LDRoff),
    path('estado_TEMPon', views.estado_TEMPon),
    path('estado_TEMPoff', views.estado_TEMPoff),
    path('estado_LCDon', views.estado_LCDon),
    path('estado_LCDoff', views.estado_LCDoff),
    path('medicion', views.medicion),
]
