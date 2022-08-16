from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("slideshow/", hello.views.slideshow, name="slideshow"),
    path("slideshow-api/", hello.views.slideshow_api, name="slideshow-api"),
    path("slideshow-api-sender/", hello.views.slideshow_api_sender, name="slideshow-api-sender"),
    path("create-slideshow/", hello.views.create_slideshow, name="create-slideshow"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
