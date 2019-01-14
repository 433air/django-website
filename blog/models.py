# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone
# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=128,unique=True)

	def __str__(self):
		return  self.name

class Message(models.Model):
	tag = models.ForeignKey(Tag)
	title = models.CharField(max_length=128)
	content = models.TextField()
	pub_date = models.DateTimeField(default=timezone.now)
	views = models.IntegerField(default=0)
	objects = models.Manager()
	
	def __str__(self):
		return  self.title