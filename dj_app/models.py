#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#coding: utf-8

from django.db import models
#from mptt.models import MPTTModel, TreeForeignKey
from tinymce import models as tinymce_models
from django.forms.widgets import *
from filebrowser.fields import FileBrowseField

# Create your models here.
class Page(models.Model):
  #поле "имя" - должно быть уникально.
  name = models.CharField(max_length=50, unique=True, verbose_name=u"Название")
  #короткое описание, показывается на карте и в отображении списком
  short = models.CharField(max_length=255, verbose_name=u"Короткое описание", null=True, blank=True) 
  #Полный текст описания фирмы
  description = tinymce_models.HTMLField(verbose_name=u"Текст описания")
  #изображение
  logo = FileBrowseField(u"Изображение", max_length=200, directory="images/",  blank=True, null=True)
  #ключевые слова
  meta_key = models.CharField(max_length=100, verbose_name=u"SEO-ключевые слова", null=True, blank=True)
  meta_description = models.CharField(max_length=100, verbose_name=u"SEO-описание", null=True, blank=True) 
  
  def __unicode__(self): #дополнительное поле, определяет информацию. выводимю на экран
    return self.name
    
  def admin_image(self):
    return '<img width="60" height="60" src="/%s"/>' % self.logo
    
  admin_image.short_description = u"Изображение"
  admin_image.allow_tags = True
    
  class Meta:
    verbose_name = u"Страницу"
    verbose_name_plural = u"Страницы"   

class PageImage(models.Model):
  image = FileBrowseField(u"Изображение", max_length=200, directory="images/")
  project = models.ForeignKey(Page)
  def admin_image(self):
    return '<img width="60" height="60" src="/%s"/>' % self.image
        
  admin_image.short_description = u"Изображение"
  admin_image.allow_tags = True

  def __unicode__(self): #дополнительное поле, определяет информацию. выводимю на экран
    return ""
  
  class Meta:
    verbose_name = u"Изображение страницы"
    verbose_name_plural = u"Дополнительные изображения страниц"