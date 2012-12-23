# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dj_app.models import *
from django.template import RequestContext, Context
from django import forms
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import *

# Create your views here.
def index(request):
  return render_to_response('app/layout.html', context_instance = RequestContext(request))