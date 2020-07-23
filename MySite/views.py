from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def portfolio(request):
    return render(request, 'portfolio.html', {})


def PostList(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'PostList.html',
                  {'page':page,
                   'posts': posts})


def PostDetail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,)
    return render(request,
                  'PostDetail.html',
                  {'post': post})
