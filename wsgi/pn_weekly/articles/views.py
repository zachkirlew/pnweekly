# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, Http404, QueryDict
from django.shortcuts import render, get_object_or_404, redirect

from articles.ArticleSerializer import ArticleSerializer, CommentSerializer
from articles.models import Article, Comment
from users.models import CustomUser
from users.views import logged_in

appname = 'PN Weekly'


# index page
def index(request):
    filter_category = request.GET.get('filter_category')

    if filter_category:
        articles = Article.objects.filter(category=filter_category).order_by('-published_at')
    else:
        articles = Article.objects.all().order_by('-published_at')

    paginator = Paginator(articles, 10)  # Show 10 articles per page

    page = request.GET.get('page')
    try:
        articles_paged = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles_paged = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles_paged = paginator.page(paginator.num_pages)

    context = {
        'appname': appname,
        'articles': articles_paged,
        'filter_category': filter_category
    }

    return render(request, 'articles/index.html', context)


# POST : like article
@logged_in
def like_article(request):
    if request.method == "POST":
        try:
            article_id = request.POST['articleId']
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return JsonResponse(status=404, data={'status': 'false', 'message': "Resource not found"})

        if request.user.is_authenticated:

            user_id = request.user.id
            user = CustomUser.objects.get(pk=user_id)

            # if user has like article, remove like
            try:
                likes = article.likes.get(pk=user.id)
                article.likes.remove(user.id)

            # if they haven't add like
            except CustomUser.DoesNotExist:

                article.likes.add(user)

                return JsonResponse({'likes': article.likes.count(),
                                     'status': True})

            serializer = ArticleSerializer(article)

        return JsonResponse({'likes': article.likes.count(),
                             'status': False})
    else:
        return JsonResponse(status=405, data={'status': 'false', 'message': "Method not allowed"})


@logged_in
def post_comment(request):
    if request.method == "POST":
        try:
            article_id = request.POST['articleId']
            comment_text = request.POST['comment']
            article = Article.objects.get(pk=article_id)

            user_id = request.user.id
            user = CustomUser.objects.get(pk=user_id)

            comment = Comment(article=article, user=user, text=comment_text)
            comment.save()

            serializer = CommentSerializer(comment)

            return JsonResponse(serializer.data)
        except Article.DoesNotExist:
            return JsonResponse(status=404, data={'status': 'false', 'message': "Resource not found"})
    else:
        return JsonResponse(status=405, data={'status': 'false', 'message': "Method not allowed"})


@logged_in
def delete_comment(request):
    if request.method == "DELETE":

        # if exists, get body data
        dict = QueryDict(request.body)

        # edit variables
        comment_id = dict.get('commentId')

        comment = get_object_or_404(Comment, pk=comment_id)
        # only allow people to delete if they are the owner of the comment
        if comment.user_id == request.user.id:

            comment.delete()

            return JsonResponse({'status': 'deleted'})
        else:
            raise Http404
    else:
        return JsonResponse(status=405, data={'status': 'false', 'message': "Method not allowed"})


# detail article view
def article_detail(request, article_id):
    # Get article for context
    article = get_object_or_404(Article, pk=article_id)

    # Get  all article comments for that article
    comments = Comment.objects.filter(article_id=article_id)

    comments = list(comments)  # convert to list object

    context = {
        'appname': appname,
        'article': article,
        'comments': comments
    }
    return render(request, 'articles/article-detail.html', context)



