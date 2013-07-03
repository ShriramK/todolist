from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.html import escape

# Create your models here.

class DateTime(models.Model):
	datetime = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return unicode(self.datetime.strftime("%b %d, %Y, %I:%M %p"))

class Item(models.Model):
	name = models.CharField(max_length=60)
	created = models.ForeignKey(DateTime)
	user = models.ForeignKey(User, blank=True, null=True)
	progress = models.IntegerField(default=0)
	priority = models.IntegerField(default=0)
	difficulty = models.IntegerField(default=0)
	done = models.BooleanField(default=False)
	onhold = models.BooleanField(default=True)
	
	def mark_done(self):
		return "<a href='%s'>Done</a>" % \
		reverse("todo.views.mark_done", args=[self.pk])
	mark_done.allow_tags = True
	
	def progress_(self):
		return "<div style='width: 100px; border: 1px solid #ccc;'>" + \
		"<div style='height: 4px; width: %dpx; background: #555; '></div></div>" % self.progress
	progress_.allow_tags = True

	def toggle_onhold(self):
		return "<a href='%s'>OnHold</a>" % \
		reverse("todo.views.toggle_onhold", \
		args=[self.pk])
	toggle_onhold.allow_tags = True
	
	def delete_item(self):
		return "<a href='%s'>Delete</a>" % \
		reverse("todo.views.delete_item", \
		args=[self.pk])
	delete_item.allow_tags = True

class ItemAdmin(admin.ModelAdmin):
	list_display = ["name", "priority", "difficulty", "user", "created", "progress_", "mark_done",  "done", "toggle_onhold", "onhold", "delete_item"]
	search_fields = ["name"]

class ItemInline(admin.TabularInline):
	model = Item

class DateAdmin(admin.ModelAdmin):
	list_display = ["datetime"]
	inlines = [ItemInline]
	
	def response_add(self, request, obj, post_url_continue='../%s/'):
		""" Determines the HttpResponse for the add_view stage. """
		opts = obj._meta
		pk_value = obj._get_pk_val()
		
		msg = "Item(s) were added successfully."
		# Here, we distinguish between different save types by checking for 
		# the presence of keys in request.POST.
		if request.POST.has_key("_continue"):
			self.message_user(request_msg + ' ' + ("You may edit again below."))
			if request.POST.has_key("_popup"):
				post_url_continue += "?_popup=1"
			return HttpResponseRedirect(post_url_continue % pk_value)
		
		if request.POST.has_key("_popup"):
			return HttpResponse(
				'<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");'
				'</script>' % (escape(pk_value), escape(obj)))
		elif request.POST.has_key("_addanother"):
			self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
			return HttpResponseRedirect(request.path)
		else:
			self.message_user(request, msg)
			for item in Item.objects.filter(created=obj):
				if not item.user:
					item.user = request.user
					item.save()
			return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

admin.site.register(Item, ItemAdmin)
admin.site.register(DateTime, DateAdmin)
