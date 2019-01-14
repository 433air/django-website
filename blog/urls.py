# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
	url(u'^$', views.index, name = 'index'),
	url(u'^about', views.about, name = 'about'),
	#url(r'^post/tag=(?P<tag>[0-9-A-Z-a-z]+)&page=(?P<page>[0-9])/$', views.post, name = 'post'),
	url(u'^post$', views.post, name = 'post'),
	url(u'^contact', views.contact, name = 'contact'),
	url(u'^detail/(?P<blog_id>\d+)/$', views.detail, name = 'detail'),
	url(u'^newpost', views.newpost, name = 'newpost'),
    url(r'^upload_image$', views.upload_image, name = 'upload_image'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)