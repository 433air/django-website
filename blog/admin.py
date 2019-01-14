# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
# Register your models here.

class MessageAdmin(admin.ModelAdmin):
	list_display = ['tag', 'title', 'content', 'pub_date', 'views']

admin.site.register(models.Tag)
admin.site.register(models.Message, MessageAdmin)
