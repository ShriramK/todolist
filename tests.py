"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime
from django.db import models
from django.test import TestCase
from todo.models import *

class SimpleTest(TestCase):
	def setUp(self):
		created_date_time = DateTime.objects.create()
		self.bread = Item.objects.create(name='Butter', created=created_date_time, user=User(), progress=100, priority=1, difficulty=1, done=False, onhold=True)
		
		created_date_time = DateTime.objects.create()
		self.sandwich = Item.objects.create(name='Sandwich', created=created_date_time, user=User(), progress=100, priority=1, difficulty=1, done=False, onhold=True)

		self.items = [self.bread, self.sandwich]
	
	def test_mark_done(self):
		"""
		Tests that an item's mark_done is called
		"""
		for each in self.items:
			self.assertEqual(each.mark_done(), "<a href='%s'>Done</a>" % \
		reverse("todo.views.mark_done", args=[each.pk]))

	def test_progress_(self):
		"""
		Tests that an item's added to the list.
		"""
		for each in self.items:
			self.assertEqual(each.progress_(), "<div style='width: 100px; border: 1px solid #ccc;'>" + \
			"<div style='height: 4px; width: %dpx; background: #555; '></div></div>" % each.progress)

	def test_onhold(self):
		"""
		Tests that an item's put on hold
		"""
		for each in self.items:
			self.assertEqual(each.toggle_onhold(),
			"<a href='%s'>OnHold</a>" % \
			reverse("todo.views.toggle_onhold", \
			args=[each.pk]))

	def test_delete_item(self):
		"""
		Tests that an item's deleted
		"""
		for each in self.items:
			self.assertEqual(each.delete_item(),
			"<a href='%s'>Delete</a>" % \
			reverse("todo.views.delete_item", \
			args=[each.pk]))
