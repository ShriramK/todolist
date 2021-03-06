from django.conf import settings
from django.contrib import admin
#from django.contrib.admin.templatetags.admin_static import static
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
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
	onhold = models.BooleanField(default=False)
	
	def progress_(self):
		return """
			<div id="progress_cont_%s" class="progress_cont">
				<div id="progress_btns_%s" class="progress_btns">
					<ul>
						<li>10</li>
						<li>20</li>
						<li>30</li>
						<li>40</li>
						<li>50</li>
						<li>60</li>
						<li>70</li>
						<li>80</li>
						<li>90</li>
						<li>100</li>
					</ul>
				</div>
				<div id="progress_on_%s" class="progress_on">&nbsp;</div>
				<div id="progress_%s" style="visibility: hidden"></div>
			</div>
			""" % (self.pk, self.pk, self.pk, self.pk)

	progress_.allow_tags = True

	def delete_item(self):
		return "<a href='%s'>Delete</a>" % \
		reverse("todo.views.delete_item", \
		args=[self.pk])
	delete_item.allow_tags = True

	def onhold_(self):
		if self.onhold:
			btn = "<div id='onhold_%s'><img alt='True' src='%sicon-on.gif'/></div>"
		else:
			btn = "<div id='onhold_%s'><img alt='True' src='%sicon-off.gif'/></div>"
		return btn % (self.pk, settings.MEDIA_URL)
	onhold_.allow_tags = True
	onhold_.admin_order_field = "onhold"

	def done_(self):
		if self.done:
			btn = "<div id='done_%s'><img alt='True' \
			src='%sicon-on.gif' /></div>"
		else:
			btn = "<div id='done_%s'><img alt='True' \
			src='%sicon-off.gif' /></div>"
		return btn % (self.pk, settings.MEDIA_URL)
	done_.allow_tags = True
	done_.admin_order_field = "done"

class ItemAdmin(admin.ModelAdmin):
	list_display = ["name", "priority", "difficulty", "user", "created", "progress_", "done_", "onhold_", "delete_item"]
	list_filter = ["priority", "difficulty", "user"]
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
			#return render(request, "todo/item/change_list.html")

admin.site.register(Item, ItemAdmin)
admin.site.register(DateTime, DateAdmin)
