# -*- coding: utf-8 -*-
from django import forms
from .models import Message

class MessagePostForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('title', 'tag', 'content')