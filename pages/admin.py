from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Page

# Register your models here.
class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
	list_display = ('id', 'title', 'page_short_description', 'slug', 'is_published', 'page_link_location', 'white_background_modify', 'full_width_modify')
	list_display_links = ('id', 'title')
	fields = ('title', 'content', 'is_published', 'page_link_location', 'white_background', 'full_width')
	search_fields = ('title', 'content', 'id')
	list_per_page = 50

	def render_change_form(self, request, context, *args, **kwargs):
		self.change_form_template = 'admin/pages/change_form_help_text.html'
		extra = {
			'help_text': "Hint: To add a contact form anywhere on the page, simply add \" [contact_form] \" in the main content."
		}

		context.update(extra)
		return super(PageAdmin, self).render_change_form(request,
			context, *args, **kwargs)

admin.site.register(Page, PageAdmin)