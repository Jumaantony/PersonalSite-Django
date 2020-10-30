from django import template
from ..models import Post, Project
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('latest_projects.html')
def show_latest_projects(count=5):
    latest_projects = Project.objects.filter(status='publish').order_by('-publish')[:count]
    return {'latest_projects': latest_projects}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
