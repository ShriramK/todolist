# Create your views here.

from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from todo.models import *

@staff_member_required
def mark_done(request, pk):
	item = Item.objects.get(pk=pk)
	item.done = True
	item.save()
	return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

@staff_member_required
def toggle_onhold(request, pk):
	item = Item.objects.get(pk=pk)
	if item.onhold:
		item.onhold = False
	else:
		item.onhold = True
	item.save()
	return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

@staff_member_required
def delete_item(request, pk):
	item = Item.objects.get(pk=pk)
	print type(item)
	print item.name		
	if item is None:
		print "Cannot delete item. doesn't exist"
	else:
		print "Deleting item"
		item.delete()
	print type(item)
	print item.name
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

