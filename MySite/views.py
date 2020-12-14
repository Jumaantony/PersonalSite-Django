from django.shortcuts import render, get_object_or_404
from .models import Post, Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.views import generic
from taggit.models import Tag
from django.db.models import Count
from django.core.mail import send_mail


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def portfolio(request):
    return render(request, 'portfolio.html', {})


def PostList(request, tag_slug=None):
    posts = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

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
                  {'page': page,
                   'posts': posts,
                   'tag': tag, })


def PostDetail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day, )

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

    # list of similar functions
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                    .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'PostDetail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


class Projects(generic.ListView):
    queryset = Project.objects.filter(status='publish').order_by('-publish')
    template_name = 'projects.html'
    paginate_by = 3


class ProjectDetail(generic.DetailView):
    model = Project
    template_name = 'ProjectDetail.html'


def Contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        # sending emails
        send_mail(
            'message from' + message_name, # subject
            message, # message
            message_email , # from
            ['jumaantony840@gmail.com'], # to
        )

        return render(request, 'contact.html',
                      {'message_name': "Hello " + message_name + "! We will resopnd to you shortly..."})
    else:
        return render(request, 'contact.html', {})
