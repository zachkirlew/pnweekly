import datetime

import requests
from django.core.management import BaseCommand, CommandError
from django.db.models import Q
from django.template.loader import render_to_string

from articles.models import Article
from users.models import CustomUser

class Command(BaseCommand):
    # Show this when the user types help
    help = "Get new articles and updates database"

    # A command must define handle()
    def handle(self, *args, **options):

        news_data = get_news_data()
        articles = deserialize_news_data(news_data)

        # if there are new articles generally
        if len(articles) > 0:

            # send email for each user with pref alert on
            email_alert_users = CustomUser.objects.filter(Q(business=True) | Q(music=True)
                                                          | Q(sport=True) | Q(technology=True))
            for user in email_alert_users:

                categories = []
                user_articles = []

                # get all user pref categories and filter all new articles by preferences
                if user.business:
                    user_articles.extend([article for article in articles if article.category == 'business'])
                    categories.append('business')
                if user.music:
                    user_articles.extend([article for article in articles if article.category == 'music'])
                    categories.append('music')
                if user.sport:
                    user_articles.extend([article for article in articles if article.category == 'sport'])
                    categories.append('sport')
                if user.technology:
                    user_articles.extend([article for article in articles if article.category == 'technology'])
                    categories.append('technology')

                # format alert info text for email
                if len(categories) > 1:
                    alert_categories = (', '.join(categories[:-1]) + ' & ' + categories[-1])
                elif len(categories) == 1:
                    alert_categories = categories[0]

                # if there are new articles that the user will want to see
                if len(user_articles) > 0:

                    user_articles.sort(key=lambda article: article.published_at, reverse=True)


                    msg_html = render_to_string('templated_email/article_alert.html', {'user': user,
                                                                                       'articles': user_articles,
                                                                                       'url': 'http://pnweekly-group8.apps.devcloud.eecs.qmul.ac.uk/',
                                                                                       'alert_categories': alert_categories})
                    try:
                        self.stdout.write(self.style.WARNING("About to send email to %s" % user.email))

                        send_mail(
                            'New articles have been posted! ',
                            'Hey ' + user.first_name + ' new interesting articles you will be interested in have been posted!',
                            'PN Weekly',
                            [user.email],
                            html_message=msg_html
                        )

                        self.stdout.write(self.style.SUCCESS('Successfully sent email to "%s"' % user.email))
                    except Exception:
                        raise CommandError('Failed to send test email')


def get_category_name(source_name):
    category = ''
    if source_name == 'Business Insider (UK)':
        category = 'business'
    elif source_name == 'ESPN':
        category = 'sport'
    elif source_name == 'MTV News (UK)':
        category = 'music'
    elif source_name == 'TechCrunch':
        category = 'technology'

    return category


# Deserialize and save article objects to db
def deserialize_news_data(data):

    # list of articles
    articles = []

    # get count of articles
    article_count = len(data['articles'])

    i = 0

    # iterate through each article and save object to database
    while i < article_count:
        source_name = data['articles'][i]['source']['name']
        author = data['articles'][i]['author']

        # Handles null author values from News API
        if author is None:
            author = source_name

        title = data['articles'][i]['title']
        description = data['articles'][i]['description']
        image_url = data['articles'][i]['urlToImage']
        url = data['articles'][i]['url']
        published_at_str = str(data['articles'][i]['publishedAt'])



        try:
            published_at = datetime.datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            published_at = datetime.datetime.now()

        category = get_category_name(source_name)

        # only add article if url doesn't exist in DB
        if not Article.objects.filter(url=url).exists():
            article = Article(source_name=source_name, author=author, title=title,
                              description=description, image_url=image_url, url=url,
                              published_at=published_at, category=category)
            article.save()
            articles.append(article)

        i = i + 1

    return articles


# Get json news data from News API
def get_news_data():
    # initiate news api request

    api_key = 'd153520382a54de5ae49fc02039645fd'
    url = "https://newsapi.org/v2/top-headlines?sources=techcrunch,mtv-news-uk,espn,business-insider-uk&apiKey=" + api_key
    r = requests.get(url)

    data = r.json()

    return data
