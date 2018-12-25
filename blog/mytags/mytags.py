#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.utils.html import format_html 

register = template.Library()

@register.filter
def mytags_upper(val):
	return val.upper()

@register.simple_tag
def circle_page(curr_page, loop_page):
	offset = abs(curr_page - loop_page)
	if offset < 2:
		if curr_page == loop_page:
			page_ele = '<a class="btn btn-primary float-center active " href="?page=%s">%s</a>' %(loop_page, loop_page)
		else:
			page_ele = '<a class="btn btn-primary float-center " href="?page=%s">%s</a>' %(loop_page, loop_page)
	
		return format_html(page_ele)
	return ''

