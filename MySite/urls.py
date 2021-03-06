from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'MySite'

urlpatterns = [
    path('index.html', views.index, name='index'),

    path('portfolio.html', views.portfolio, name='portfolio'),

    path('PostList.html', views.PostList, name='PostList'),

    path('tag/<slug:tag_slug>/', views.PostList, name='PostList_by_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.PostDetail, name='PostDetail'),

    path('feed/', LatestPostsFeed(), name='post_feed'),

    path('projects.html', views.Projects.as_view(), name='Projects'),

    path('<slug:slug>/', views.ProjectDetail.as_view(), name='ProjectDetail'),

    path('contact.html', views.Contact, name='Contact'),
]
