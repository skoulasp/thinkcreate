from ckeditor_uploader.fields import RichTextUploadingField
from blog.models import generate_unique_slug
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.html import format_html, strip_tags
from django.template.defaultfilters import truncatechars

# Create your models here.
class Page(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True)
	content = RichTextUploadingField()
	is_published = models.BooleanField(default=True)
	NAVBAR = 'Navbar'
	FOOTER = 'Footer'
	BOTH = 'Both Navbar & Footer'
	DISABLED = 'Page Disabled'
	DISPLAY_CHOICES = [
		(NAVBAR, 'Navbar'),
		(FOOTER, 'Footer'),
		(BOTH, 'Both Navbar & Footer'),
		(DISABLED, 'Page Disabled'),
	]
	page_link_location = models.CharField(
		max_length=20,
		choices=DISPLAY_CHOICES,
		default=NAVBAR,
	)
	page_order = models.PositiveIntegerField(default=0, blank=False, null=False)
	white_background = models.BooleanField(verbose_name='Use a white background for this page', default=False)
	full_width = models.BooleanField(verbose_name='Make this page take up the full width of the viewport', default=False)

	class Meta(object):
		ordering = ['page_order']

	def save(self, *args, **kwargs):
		if self.slug:  # edit
			if slugify(self.title) != self.slug:
				self.slug = generate_unique_slug(Page, self.title)
		else:  # create
			self.slug = generate_unique_slug(Page, self.title)
		super(Page, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	def page_short_description(self):
		return strip_tags(truncatechars(self.content, 50))

	def white_background_modify(self):
		return self.white_background

	def full_width_modify(self):
		return self.full_width


	page_short_description.short_description = u'Page Content'
	white_background_modify.short_description = u'Full White Background'
	white_background_modify.boolean = True
	full_width_modify.short_description = u'Full Width'
	full_width_modify.boolean = True


