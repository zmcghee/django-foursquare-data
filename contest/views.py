import httplib, time, datetime, urlparse

from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import render_to_response
from django.utils import simplejson

import djangofoursquare.oauth
import foursquare.models as foursquare
from foursquare.utils import *
from foursquare.views import *

def homepage(request):
	if request.META['QUERY_STRING'] == 'error':
		notice = request.session['notice']
	elif request.META['QUERY_STRING'] == 'success':
		notice = 'You were successfully authenticated.'
	else:
		notice = None
	return render_to_response('contest.html', { 'notice': notice } )
	
def history(request):
	users = foursquare.User.objects.all()
	save_history_to_database(users)
	return HttpResponse('Done. <a href="/">Back</a>')