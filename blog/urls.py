from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^about', views.about, name = 'about'),
	#url(r'^post/tag=(?P<tag>[0-9-A-Z-a-z]+)&page=(?P<page>[0-9])/$', views.post, name = 'post'),
	url(r'^post$', views.post, name = 'post'),
	url(r'^contact', views.contact, name = 'contact'),
	url(r'^detail/(?P<blog_id>\d+)/$', views.detail, name = 'detail'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)