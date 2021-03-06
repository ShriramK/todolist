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
	if mode == 'jquery':
		print 'settings.MEDIA_ROOT\n'
		print settings.MEDIA_ROOT
		f = open((settings.MEDIA_ROOT+'\jquery.min.js').replace('\\','/'))
		return HttpResponse(f.read())
	f = None
	val = ''
	if mode == 'on':
		val = 'on'
	else:
		val = 'off'
	f = open((settings.MEDIA_ROOT+'\icon-'+val+'.gif').replace('\\','/'))
	return HttpResponse(f.read(), mimetype="image/gif")

def progress(request, pk):
	"""Set task progress."""
	p = request.POST
	if "progress" in p:
		item = Item.objects.get(pk=pk)
		item.progress = int(p["progress"])
		item.save()
	return HttpResponse('')
	#return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

