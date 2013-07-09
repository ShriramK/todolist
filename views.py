# Create your views here.

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from todo.models import *

@staff_member_required
def delete_item(request, pk):
	Item.objects.filter(pk=pk).delete()
	return HttpResponseRedirect(reverse("admin:todo_item_changelist"))
	
@staff_member_required
def onhold_done(request, mode, action, pk):
	"""Toggle Done / Onhold on/off."""
	item = Item.objects.get(pk=pk)

	print 'request '
	print request

	if action == "on":
		if mode == "done": item.done = True
		elif mode == "onhold": item.onhold = True
	elif action == "off":
		if mode == "done": item.done = False
		elif mode == "onhold": item.onhold = False
	
	item.save()
	return HttpResponse('')

@staff_member_required
def media(request, mode):
	"""
	Serve icon-on|off.gif media file and jquery.js
	""" 
	f = None
	val = ''
	#if 'icon-on.gif' in request.path:
	if mode == 'on':
		val = 'on'
	else:
		val = 'off'
	f= open((settings.MEDIA_ROOT+'\icon-'+val+'.gif').replace('\\','/'))
	return HttpResponse(f.read(), mimetype="image/gif")

'''
@staff_member_required
def changelist(request):
	return render(request, 'todo/item/change_list.html')
'''