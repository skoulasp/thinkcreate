from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from accounts.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars


# Create your models here.

class Category(models.Model):
	title = models.CharField(max_length=20, blank=True)
	
	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.title


class Post(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True)
	content = RichTextUploadingField()
	author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='blog_posts')
	date = models.DateTimeField(auto_now_add=True)
	categories = models.ManyToManyField(Category, null=True, blank=True)
	is_published = models.BooleanField(default=True)
	featured = models.BooleanField(verbose_name='Featured Post', default=False)
	comments_allowed = models.BooleanField(default=True)
	comments_require_approval = models.BooleanField(default=False)
	unregistered_commenters = models.BooleanField(default=True)

	def total_comments(self):
		c = str(self.comments.count())
		url = u'../comment/?post__id__exact=%d' % self.id
		return format_html(u'<a href="%s">%s</a>' % (url, c) )

	total_comments.allow_tags = True

	def get_approved_comments(self):
		approved_comments = self.comments.filter(active=True).count()
		return approved_comments


	def save(self, *args, **kwargs):
		if self.slug:  # edit
			if slugify(self.title) != self.slug:
				self.slug = generate_unique_slug(Post, self.title)
		else:  # create
			self.slug = generate_unique_slug(Post, self.title)
		if self.featured:
			try:
				temp = Post.objects.get(featured=True)
				if self != temp:
					temp.featured = False
					temp.save()
			except Post.DoesNotExist:
					pass
		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=200)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date']

	def get_total_likes(self):
		return self.likes.users.count()

	get_total_likes.short_description = 'Total Likes'

	def get_total_dislikes(self):
		return self.dislikes.users.count()

	get_total_dislikes.short_description = 'Total Dislikes'

	def __str__(self):
		return 'Comment {} by {}'.format(self.body, self.name)

	def body_short_description(self):
		return truncatechars(self.body, 30)

	def name_modify(self):
		return self.name

	body_short_description.short_description = u'Content'
	name_modify.short_description = u'Name / User'



class Like(models.Model):
    comment = models.OneToOneField(Comment, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='comment_likes')

    def __str__(self):
        return str(self.comment.body)[:30]

class Dislike(models.Model):
    comment = models.OneToOneField(Comment, related_name="dislikes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='comment_dislikes')

    def __str__(self):
        return str(self.comment.body)[:30]


def generate_unique_slug(klass, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

