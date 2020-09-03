from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post, Comment, Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.views import generic



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
   

    # list of active comments
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # comment posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create a new comment but do not save in the database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm

    return render(request,
                  'PostDetail.html',
                  {'post': post,
                  'comments': comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form})
                  

class Projects(generic.ListView):
    queryset = Project.objects.filter(status ='publish' ).order_by('-publish')
    template_name = 'projects.html'
    paginate_by = 3


class ProjectDetail(generic.DetailView):
    model = Project
    template_name = 'ProjectDetail.html'


def Contact(request):
    return render(request, 'contact.html', {})
    
