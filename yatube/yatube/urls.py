"""yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # registration and authorization
    path("auth/", include("users.urls")),

    # if the required template for /auth was not found in the users.urls file,
    # we look for matches in the django.contrib.auth.urls file
    path("auth/", include("django.contrib.auth.urls")),

    # admin section
    path("adminka/", admin.site.urls),

    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='spec'),

    # API Documentation
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),

    # import urls from api application
    path('api/v1/', include('api.urls')),

    # import urls from posts application
    path("", include("posts.urls")),
]

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

# We are adding the ability to upload files, which means that these files should be available in development mode.
# This allows files in the directory specified in MEDIA_ROOT to be accessed by name, via the MEDIA_URL prefix
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
