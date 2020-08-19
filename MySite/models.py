from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique_for_date='publish')
    featured_image = models.ImageField(upload_to='featuredImage/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('MySite:PostDetail', args=[self.publish.year,
                                                  self.publish.month,
                                                  self.publish.day,
                                                  self.slug])


class Project(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('publish','Published')
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique_for_date='publish')
    featured_img = models.ImageField(upload_to='ProjectImages')
    body = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default='draft')

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager
    

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('MySite:ProjectDetail', args=[self.publish.year,
                                                  self.publish.month,
                                                  self.publish.day,
                                                  self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated  = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
