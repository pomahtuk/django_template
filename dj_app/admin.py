#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dj_app.models import *
from django.contrib import admin
from dj_app.widgets import *
from django import forms

class MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

class PageImageAdmin(MyModelAdmin):
  pass

class PageImageInline(admin.StackedInline):
  model = PageImage
  max_num=10
  extra=0

class PageAdmin(admin.ModelAdmin):
  list_display = ('admin_image', 'name', 'short') 
  search_fields = ['name'] 
  ordering = ('-id',) 
  list_filter = ('short',)
  inlines = [PageImageInline,]   
  fieldsets = [ 
    ('Основное', {'fields': ['name', 'short', 'description']}),
    ('Изображения', {'fields': ['logo']}),
    ('Мета', {'fields': ['meta_key','meta_description']}),    
  ] 
  # class form(forms.ModelForm): 
  #   class Meta:
  #     widgets = {
  #       'location':LocationWidget,
  #     }  
  
admin.site.register(Page, PageAdmin)
admin.site.register(PageImage, PageImageAdmin)