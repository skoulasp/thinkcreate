from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse ,HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, Count
from .models import Post, Comment, Like, Dislike
from settings.models import SiteConfiguration
from pages.models import Page
from .forms import CommentForm
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, RedirectView
from django.template import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def blog(request):
	category_count = get_category_count()
	most_recent = Post.objects.order_by('-date')[:3]
	settings = SiteConfiguration.objects.first()
	posts = Post.objects.all().filter(is_published=True).order_by('-date')
	comments = None
	for post in posts:
		comments = post.comments.filter(active=True).count()
	if (settings):
		paginator = Paginator(posts, settings.posts_per_page)
	else:
		paginator = Paginator(posts, 5)
	page = request.GET.get('page')
	paged_posts = paginator.get_page(page)
	context = {
		'posts': paged_posts,
		'comments': comments,
		'posts_list': True,
		'category_count': category_count,
		'most_recent': most_recent,
		'order': 'latest',
	}
	return render(request, "blog/feed.html", context)

def post(request, slug):
	post = get_object_or_404(Post, slug=slug)

	comments = post.comments.filter(active=True)
	new_comment = None
	message = None
	comment_form = CommentForm(request=request)
	context = {
		'post': post,
		'comments': comments,
		'new_comment': new_comment,
		'comment_form': comment_form,
	}

	if request.method == 'POST':
		comment_form = CommentForm(request=request, data=request.POST)
		if comment_form.is_valid():

			if request.user.is_authenticated:
				new_comment = comment_form.save(commit=False)
				new_comment.user = request.user
				new_comment.post = post
			else:
				new_comment = comment_form.save(commit=False)
				new_comment.post = post

			if post.comments_require_approval:
				new_comment.active = False
				messages.success(request, 'Your comment has been submitted and is pending approval.')

			else:
				messages.success(request, 'Comment posted successfully.')
				
			new_comment.save()

			return HttpResponseRedirect(request.path_info)
		else:
			comment_form = CommentForm(request=request, data=request.POST)
	return render(request, "blog/post.html", context)

def search(request):
	posts = Post.objects.all().filter(is_published=True)
	pages = Page.objects.all().filter(is_published=True)
	query = request.GET.get('q')
	if query:
		posts = posts.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) 
			).distinct()

		search_pages = pages.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) 
			).distinct()
		
		context = {
			'posts': posts,
			'search_pages': search_pages,
			'query': query
		}

		return render(request, "blog/search_results.html", context)

def cat_search(request):
	cat_query = request.GET.get('q')
	if cat_query:
		posts = Post.objects.all().filter(categories__title__contains=cat_query)
		context = {
			'categorized_posts': posts,
			'query': cat_query
		}
		return render(request, "blog/search_results.html", context)

def post_search(request):
	posts = Post.objects.all()
	query = request.GET.get('q')

	if query:
		onlyposts = posts.filter(
		Q(title__icontains=query) |
		Q(content__icontains=query) 
		).distinct()

		context = {
			'onlyposts': onlyposts,
			'query': query
		}
		return render(request, "blog/search_results.html", context)

def get_category_count():
	queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
	return queryset


def order_by(request):
    category_count = get_category_count()
    order = request.GET.get('by')
    most_recent = Post.objects.order_by('-date')[:3]
    settings = SiteConfiguration.objects.first()
    if order == 'latest':
        ordered_posts = Post.objects.all().filter(is_published=True).order_by('-date')
    elif order == 'oldest':
        ordered_posts = Post.objects.all().filter(is_published=True).order_by('date')
    elif order == 'author_a-z':
        ordered_posts = Post.objects.all().filter(is_published=True).order_by('author')
    elif order == 'author_z-a':
        ordered_posts = Post.objects.all().filter(is_published=True).order_by('-author')
    else:
        # Default to ordering by latest date if order parameter is not specified
        ordered_posts = Post.objects.all().filter(is_published=True).order_by('-date')

    paginator = Paginator(ordered_posts, settings.posts_per_page)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)

    context = {
        'ordered_posts': paged_posts,
        'order': order,
        'category_count': category_count,
        'most_recent': most_recent,
    }

    return render(request, "blog/feed.html", context)


class UpdateCommentVote(LoginRequiredMixin, View):
	login_url = '/account/login/'

	def get(self, request, *args, **kwargs):
		comment_id = self.kwargs.get('comment_id', None)
		slug = self.kwargs.get('slug', None)
		post = get_object_or_404(Post, slug=slug)
		option = self.kwargs.get('option', None)
		comment = get_object_or_404(Comment, id=comment_id)

		try:

		    comment.dislikes
		except Comment.dislikes.RelatedObjectDoesNotExist as identifier:
		    Dislike.objects.create(comment = comment)

		try:

		    comment.likes
		except Comment.likes.RelatedObjectDoesNotExist as identifier:
		    Like.objects.create(comment = comment)

		if request.user.is_authenticated:
			if option.lower() == 'like':

				if request.user in comment.likes.users.all():
					comment.likes.users.remove(request.user)
				else:    
					comment.likes.users.add(request.user)
					comment.dislikes.users.remove(request.user)

			elif option.lower() == 'dislike':

				if request.user in comment.dislikes.users.all():
					comment.dislikes.users.remove(request.user)
				else:    
					comment.dislikes.users.add(request.user)
					comment.likes.users.remove(request.user)
			else:
			    return redirect('post', slug=slug)
		else:
			return redirect('login')
		return redirect('post', slug=slug)

class UpdateCommentVoteAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
    	comment_id = self.kwargs.get('comment_id', None)
    	slug = self.kwargs.get('slug', None)
    	post = get_object_or_404(Post, slug=slug)
    	option = self.kwargs.get('option', None) 
    	comment = get_object_or_404(Comment, id=comment_id)
    	reverse_action_like = False;
    	reverse_action_dislike = False;

    	try:
    		comment.dislikes
    	except Comment.dislikes.RelatedObjectDoesNotExist as identifier:
    		Dislike.objects.create(comment = comment)
    	try:
    		comment.likes
    	except Comment.likes.RelatedObjectDoesNotExist as identifier:
    		Like.objects.create(comment = comment)

    	if request.user.is_authenticated:
    		if option.lower() == 'like':

    			if request.user in comment.likes.users.all():
    				comment.likes.users.remove(request.user)

    				reverse_action_like = True;
    			else:
    				comment.likes.users.add(request.user)
    				comment.dislikes.users.remove(request.user)

    				reverse_action_like = False;
    		elif option.lower() == 'dislike':
    			if request.user in comment.dislikes.users.all():
    				comment.dislikes.users.remove(request.user)

    				reverse_action_dislike = True;
    			else:
    				comment.dislikes.users.add(request.user)
    				comment.likes.users.remove(request.user)

    				reverse_action_dislike = False;
    		else:
    			return redirect('post', slug=slug)
    	else:
    		return redirect('login')
    	data = {'option': option, 'reverse_action_like': reverse_action_like, 'reverse_action_dislike': reverse_action_dislike, 'total_likes': comment.get_total_likes(), 'total_dislikes': comment.get_total_dislikes(), "id": comment.id}
    	return Response(data)