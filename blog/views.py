# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.http import urlquote
# Create your views here.

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def index(request):
	all_messages = models.Message.objects.all().order_by('-id')[:5]
	for message in all_messages:
		if len(message.content) > 25:
			message.content = message.content[0:25] + '......'
	context_dict = {}
	context_dict['all_messages'] = all_messages
	return render(request, 'blog/index.html', context_dict)

def detail(request, blog_id):
	msg = models.Message.objects.get(id=int(blog_id))
	print msg.tag.name
	if msg: msg.views+=1
	msg.save()
	context_dict = {}
	context_dict['message'] = msg
	return  render(request,'blog/detail.html',context_dict)

def about(request):
	return render(request, 'blog/about.html', locals())

def contact(request):
	return render(request, 'blog/contact.html', locals())
	
import urllib
def post(request):
	page = request.GET.get('page')
	cus_list = None
	context_dict = {}
	context_dict['hastag'] = ''
	tag = request.GET.get('tag')
	if tag:
		context_dict['hastag'] = tag
		tag_id = models.Tag.objects.get(name = tag)
		cus_list = tag_id.message_set.all().order_by('-id')
	else:
		cus_list = models.Message.objects.all().order_by('-id')
	paginator = Paginator(cus_list, 5, 0)
	
	try:
		customer = paginator.page(page)
	except PageNotAnInteger:
		customer = paginator.page(1)
	except EmptyPage:
		customer = paginator.page(paginator.num_pages)
	context_dict['all_messages'] = customer
	return render(request, 'blog/post.html',context_dict) # {"all_messages": customer})
