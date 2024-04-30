from django.contrib import admin
from .models import Category, Post, Comment, Like
from django.core.exceptions import ValidationError

# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'author', 'slug', 'date', 'total_comments', 'is_published', 'comments_allowed', 'comments_require_approval', 'unregistered_commenters', 'featured')
	list_display_links = ('id', 'title', 'total_comments',)
	list_filter = ('date', 'is_published')
	list_editable = ('is_published',)
	search_fields = ('title', 'content', 'id' 'date')
	list_per_page = 50
	fields = ('title', 'content', 'categories', 'is_published', 'comments_allowed', 'comments_require_approval', 'unregistered_commenters', 'featured')
	readonly_fields = ['slug', 'author']

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'author', None) is None:
			user = request.user
			if user.is_author:
				obj.author = user
			else:
				raise ValidationError('User is not author.')
		obj.save()

admin.site.register(Category)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name_modify', 'body_short_description', 'post', 'get_total_likes', 'get_total_dislikes', 'date', 'active')
    list_display_links = ('body_short_description', 'name_modify',)
    list_filter = ('date', 'active', 'post',)
    search_fields = ('name_modify', 'email', 'body')
    actions = ['approve_comments']
    readonly_fields = ['post', 'name', 'user', 'email', 'body', 'date',]

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': context.get('show_save_and_add_another', False),
            'show_save': True,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)