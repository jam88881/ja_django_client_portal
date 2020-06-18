# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="ui-notifications.html")),
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),  # add this
    path('accounts/', include("allauth.urls")),
    path("", include("app.urls"))  # add this
]
