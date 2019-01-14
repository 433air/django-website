# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import os
import socket
import uuid

import markdown
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from . import models
from .form import MessagePostForm

# Create your views here.

def index(request):
	all_messages = models.Message.objects.all().order_by('-id')[:5]
	# for message in all_messages:   目前不打算看预览了.
	# 	if len(message.content) > 25:
	# 		message.content = message.content[0:25] + '......'
	context_dict = {}
	context_dict['all_messages'] = all_messages
	return render(request, 'blog/index.html', context_dict)

def detail(request, blog_id):
	msg = models.Message.objects.get(id=int(blog_id))
	if msg: msg.views+=1
	msg.save()

	msg.content = markdown.markdown(msg.content, 
		extensions = [
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.tables',
			'markdown.extensions.toc'
		]
	)
	context_dict = {}
	context_dict['message'] = msg
	return  render(request,'blog/detail.html',context_dict)

def about(request):
	return render(request, 'blog/about.html', locals())

def contact(request):
	return render(request, 'blog/contact.html', locals())

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

def newpost(request):
	if request.method == 'POST':
		newpostform = MessagePostForm(data=request.POST)
		if newpostform.is_valid():
			newpost = newpostform.save(commit = False)
			newpost.author = User.objects.get(id=1)
			newpost.save()
			return redirect('post')
			#倒是后试试直接跳转进detail页
		else:
			return HttpResponse('内容错误,请重新填写')
	else:
		newpostform = MessagePostForm()
		context = {'newpostform,': newpostform}
		return render(request, 'blog/newpost.html', context)

def uploadimage(request):
	if request.method == 'POST':
		myfile = request.FILES.get('teamFile',None)
		filename = str(uuid.uuid1())+os.path.splitext(myfile._name)[1]
		savename = os.path.join(os.getcwd(),'teamdoc')
		savename = os.path.join(savename,'uploadFile')
		savename = os.path.join(savename,filename)
		code = 1000
		if myfile:
			
			code = 0
		else:
			filename=''
		jsondata =json.dumps({"code":code,"msg":{"url":'/uploadFile/%s'%(filename),'filename':myfile._name}})
		return HttpResponse(jsondata,content_type="application/json")

def get_host_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
	return ip

@csrf_exempt
def upload_image(request):
	if request.method == "POST":  # 请求方法为POST时，进行处理
		myFile = request.FILES.get("editormd-image-file", None)  # 获取上传的文件，如果没有文件，则默认为None
		if myFile:
			name = request.FILES['editormd-image-file'].name
			filename = str(uuid.uuid1()) + name
			savename = os.path.join(os.getcwd(),'media')
			savename = os.path.join(savename,filename)

			with open(savename,'wb') as file:
				file.write(myFile.read())

		else:
			HttpResponse(json.dumps({'success':0,'message':'上传失败'}, ensure_ascii=False), content_type="application/json")
		return HttpResponse(json.dumps({'success':1,'message':'', 'url': get_host_ip() +'/media/%s' + name}, ensure_ascii=False), content_type="application/json")

# {
#   'success(1表示成功,0表示失败)': 1(或0),
#   'message': 'message',
#   'url(如果失败则不返回)': 'imageURL'
# }
