from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, FooterConfiguration
from django.utils.html import format_html

# Register your models here.
class SiteConfigurationAdmin(SingletonModelAdmin):
	fields = (('site_name', 'standard_styling'), 'favicon', 'navbar_logo', ('navbar_color', 'default_color',), 'color_light_or_dark', 'nav_links_position', 'hide_blog_section', 'hide_search_icon', 'hide_account_options', 'meta_tags', 'blog_section_navbar', 'set_homepage', ('homepage_HTML_title', 'append_site_name'), 'posts_per_page', 'blog_social', 'insert_custom_css')
	readonly_fields = ("default_color",)

	def default_color (self, obj):
		return format_html(u'<a href="#" onclick=\'document.getElementById("id_navbar_color").value="#228567";document.getElementById("id_navbar_color").placeholder="#228567"\' class="admin-change-btn" '
                           u'id="id_admin_unit_selected">Reset to default</a>')

	default_color.allow_tags  = True

class FooterConfigurationAdmin(SingletonModelAdmin):
	fields = ('footer_enabled', 'sticky_footer', ('footer_background_color', 'default_background_color',), ('footer_header_color', 'default_header_color'), ('footer_links_color', 'default_links_color'), ('footer_blog_color', 'default_blog_color'), ('footer_text_color', 'default_text_color'), ('social_media_icons_bg_color', 'default_social_media_icons_bg_color',), ('social_media_icons_i_color', 'default_social_media_icons_i_color',), 'about_text', 'blog_section_link', 'include_account_options', 'social_media_links_enabled', 
		('facebook_url', 'fb_active'),
		('twitter_url', 'twtr_active'),
		('instagram_url', 'insta_active'),
		('linkedin', 'in_active'),
		'new_window',
		'underline_text')

	readonly_fields = ("default_background_color", "default_header_color", "default_links_color", "default_blog_color", "default_text_color", "default_social_media_icons_bg_color", 'default_social_media_icons_i_color')

	def default_background_color (self, obj):
		return format_html(u'<a class="default_background_color-btn" href="#" onclick=\'document.getElementById("id_footer_background_color").value="#26272b";document.getElementById("id_footer_background_color").placeholder="#26272b"\' class="admin-change-btn" '
		u'id="id_admin_unit_selected">Reset to default</a>')

	def default_header_color (self, obj):
		return format_html(u'<a class="default_header_color-btn" href="#" onclick=\'document.getElementById("id_footer_header_color").value="#FFF";document.getElementById("id_footer_header_color").placeholder="#FFF"\' class="admin-change-btn" '
		u'id="id_admin_unit_selected">Reset to default</a>')

	def default_links_color (self, obj):
		return format_html(u'<a class="default_links_color-btn" href="#" onclick=\'document.getElementById("id_footer_links_color").value="#737373";document.getElementById("id_footer_links_color").placeholder="#737373"\' class="admin-change-btn" '
		u'id="id_admin_unit_selected">Reset to default</a>')

	def default_blog_color (self, obj):
		return format_html(u'<a class="default_blog_color-btn" href="#" onclick=\'document.getElementById("id_footer_blog_color").value="#FFF";document.getElementById("id_footer_blog_color").placeholder="#FFF"\' class="admin-change-btn" '
		u'id="id_admin_unit_selected">Reset to default</a>')

	def default_text_color (self, obj):
		return format_html(u'<a class="default_text_color-btn" href="#" onclick=\'document.getElementById("id_footer_text_color").value="#737373";document.getElementById("id_footer_text_color").placeholder="#737373"\' class="admin-change-btn" '
		u'id="id_admin_unit_selected">Reset to default</a>')

	def default_social_media_icons_bg_color (self, obj):
		return format_html(u'<a class="default_social_media_icons_bg_color-btn" href="#" onclick=\'document.getElementById("id_social_media_icons_bg_color").value="#33353d";document.getElementById("social_media_icons_bg_color").placeholder="#33353d"\' class="admin-change-btn" '
		u'id="id_admin_unit_selected">Reset to default</a>')

	def default_social_media_icons_i_color (self, obj):
		return format_html(u'<a class="default_social_media_icons_i_color-btn" href="#" onclick=\'document.getElementById("id_social_media_icons_i_color").value="#818a91";document.getElementById("id_social_media_icons_i_color").placeholder="#33353d"\' class="admin-change-btn" '
		u'id="id_admin_unit_selected">Reset to default</a>')

	default_background_color.allow_tags  = True
	default_header_color.allow_tags  = True
	default_text_color.allow_tags  = True
	default_social_media_icons_bg_color.allow_tags  = True
	default_social_media_icons_i_color.allow_tags  = True

admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
admin.site.register(FooterConfiguration, FooterConfigurationAdmin)

