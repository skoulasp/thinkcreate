from django.db import models
from django.db import models
from solo.models import SingletonModel
from colorfield.fields import ColorField
from pages.models import Page
from thinkcreate.storage import OverwriteStorage
from django import forms
from .forms import ChoiceForm


class SiteConfiguration(SingletonModel):
	site_name = models.CharField(max_length=30, default='ThinkCreate')
	standard_styling = models.BooleanField(verbose_name='Use standard styling for site title', default=False)
	favicon = models.ImageField(storage=OverwriteStorage(), default=None, upload_to='uploads/favicon', null=True, blank=True) 
	navbar_logo = models.ImageField(upload_to='uploads/logo', null=True, blank=True) 
	navbar_color = ColorField(default='#228567')
	DARK = 'Dark'
	VERY_DARK = 'Very Dark'
	LIGHT = 'Light'
	CHOICES = [
		(DARK, 'Dark'),
		(VERY_DARK, 'Very Dark'),
		(LIGHT, 'Light'),

	]
	color_light_or_dark = models.CharField(verbose_name='How light or dark is the navbar color you chose',
		max_length=20,
		choices=CHOICES,
		default=DARK,
	)
	CENTER = 'Center'
	RIGHT = 'Right'
	POS_CHOICES = [
		(CENTER, 'Center'),
		(RIGHT, 'Right'),

	]
	nav_links_position = models.CharField(verbose_name='Where do you want the navbar page links to appear',
		max_length=20,
		choices=POS_CHOICES,
		default=CENTER,
	)
	hide_blog_section = models.BooleanField(verbose_name='Hide blog section from navbar', default=False)
	hide_search_icon = models.BooleanField(verbose_name='Hide search function from navbar', default=False)
	hide_account_options = models.BooleanField(verbose_name='Hide login/register options from navbar', default=False)
	append_site_name = models.BooleanField(verbose_name='Append site name to homepage HTML title', default=False)
	meta_tags = models.CharField(verbose_name='Site-wide meta description tags for improved SEO', max_length=300, null=True, blank=True)
	set_homepage = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
	homepage_HTML_title = models.CharField(verbose_name='Homepage HTML title', max_length=30, null=True, blank=True)
	append_site_name = models.BooleanField(verbose_name='Append site name to homepage HTML title', default=False)
	blog_section_navbar = models.BooleanField(default=True)
	THREE = '3'
	FIVE = '5'
	TEN = '10'
	TWENTY_FIVE = '25'
	PAGINATION_CHOICES = [
		(THREE, '3'),
		(FIVE, '5'),
		(TEN, '10'),
		(TWENTY_FIVE, '25'),

	]
	posts_per_page = models.CharField(verbose_name='Number of blog posts per page',
		max_length=20,
		choices=PAGINATION_CHOICES,
		default=FIVE,
	)
	insert_custom_css = models.TextField(verbose_name='Insert custom CSS rules', null=True, blank=True)
	blog_social = models.BooleanField(verbose_name='Add social media sharing buttons to blog posts', default=True)

	def __str__(self):
		return "Site Configuration"

	class Meta:
		verbose_name = "Site Configuration"

	def __init__(self, *args, **kwargs):
		super(SiteConfiguration, self).__init__(*args, **kwargs)



class FooterConfiguration(SingletonModel):
	footer_enabled = models.BooleanField(default=True)
	sticky_footer = models.BooleanField(default=False)
	footer_background_color = ColorField(default='#26272b')
	footer_header_color = ColorField(default='#FFF')
	footer_links_color = ColorField(default='#737373')
	footer_blog_color = ColorField(default='#FFF')
	footer_text_color = ColorField(default='#737373')
	social_media_icons_bg_color = ColorField(default='#33353d')
	social_media_icons_i_color = ColorField(default='#818a91')
	about_text = models.TextField(verbose_name='Site description (About)', max_length=650, null=True, blank=True)
	blog_section_link = models.BooleanField(default=True)
	include_account_options = models.BooleanField(verbose_name='Include login/register options in the footer?', default=False)
	social_media_links_enabled = models.BooleanField(default=True)
	facebook_url = models.URLField(verbose_name='Facebook Profile URL', null=True, blank=True)
	fb_active = models.BooleanField(verbose_name='Active', default=True)
	twitter_url = models.URLField(verbose_name='Twitter Profile URL', null=True, blank=True)
	twtr_active = models.BooleanField(verbose_name='Active', default=True)
	instagram_url = models.URLField(verbose_name='Instagram Profile URL', null=True, blank=True)
	insta_active = models.BooleanField(verbose_name='Active', default=True)
	linkedin = models.URLField(verbose_name='LinkedIn Profile URL', null=True, blank=True)
	in_active = models.BooleanField(verbose_name='Active', default=True)
	new_window = models.BooleanField(verbose_name='Open social media links in a new window', default=True)
	underline_text = models.CharField(default='Copyright © 2020', max_length=100, null=True, blank=True)
	background_color = ColorField(default='#26272b')
	text_color = ColorField(default='#737373')

	def __str__(self):
		return "Footer Configuration"

	class Meta:
		verbose_name = "Footer Configuration"