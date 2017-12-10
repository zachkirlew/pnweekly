from django.conf.urls import url

from articles import views

urlpatterns = [
    # main page
    url(r'^$', views.index, name='index'),
    # login page
    url(r'^article_detail/(?P<article_id>\d+)/$', views.article_detail, name='article_detail'),
    # POST like article
    url(r'^like_article/$', views.like_article, name='like_article'),
    # GET article comments
    url(r'^get_comments/(?P<article_id>\d+)/$', views.get_comments, name='get_comments'),
    # POST article comment
    url(r'^post_comment/$', views.post_comment, name='post_comment'),
    # DELETE article comment
    url(r'^delete_comment/$', views.delete_comment, name='delete_comment'),
]
