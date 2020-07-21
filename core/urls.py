# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include 
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.dash),
    path('dash/', views.dash),
    path('status-reports/', views.status),
    path('run-reports/', views.run_reports),
    path('submitted-updates/', views.submitted_updates, name="submitted-updates"),
    path('page-user/', views.profile, name="page-user"),
    path('admin/', admin.site.urls),
    #path("", include("authentication.urls")),
    #path("", include("app.urls")),
    #path('accounts/', include("allauth.urls")),
]
