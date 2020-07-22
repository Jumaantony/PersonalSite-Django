from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def portfolio(request):
    return render(request, 'portfolio.html', {})


def PostList(request):
    posts = Post.published.all()
    return render(request,
                  'PostList.html',
                  {'posts': posts})


def PostDetail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,)
    return render(request,
                  'PostDetail.html',
                  {'post': post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'PostList.html'
