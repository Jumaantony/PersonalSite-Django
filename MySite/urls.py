from django.urls import path
from . import views

app_name = 'MySite'

urlpatterns = [
    path('index.html', views.index, name='index'),

    path('portfolio.html', views.portfolio, name='portfolio'),

    path('PostList.html', views.PostList, name='PostList'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.PostDetail, name='PostDetail'),

]