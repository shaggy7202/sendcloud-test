import pytest
import datetime
from feeds.models import Feed
from feed_items.models import FeedItem, Comment, Favourite

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils.timezone import now


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="someone", password="someUserPass12", last_login=now()
    )


@pytest.fixture
def second_user(django_user_model):
    return django_user_model.objects.create_user(
        username="someone2", password="someUserPass12", last_login=now()
    )


@pytest.fixture
def authenticated_client(client, user):
    client.login(username=user.username, password='someUserPass12')
    return client


@pytest.fixture
def feed(user):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.MINUTES
    )
    fetcher = PeriodicTask.objects.create(
        interval=schedule,
        name='test', task='sometask', enabled=False
    )
    return Feed.objects.create(
        name='FeedName',
        url='http://dummy.com',
        created_by=user,
        fetcher=fetcher
    )


@pytest.fixture
def feed_item(feed):
    return FeedItem.objects.create(
        feed=feed,
        guid='someguid',
        title='Article title',
        description='Some desc',
        publication_date=datetime.datetime.now(),
        link='http://article-link.com'
    )


@pytest.fixture
def comment(feed_item):
    return Comment.objects.create(text='Some text', feed_item=feed_item)


@pytest.fixture
def favourite(feed_item):
    return Favourite.objects.create(
        user=feed_item.feed.created_by, feed_item=feed_item
    )


@pytest.fixture
def rss_feed_xml():
    return """<?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>Some - title</title>
        <link>https://www.nu.nl/algemeen</link>
        <description>Som desc</description>
        <atom:link href="https://someref.com" rel="self"></atom:link>
        <item>
            <title>Some title</title>
            <link>https://somelink.com</link>
            <description>Some desc</description>
            <pubDate>Tue, 09 Jun 2020 23:53:52 +0200</pubDate>
            <guid isPermaLink="false">https://somelink/-/102030/</guid>
        </item>
        <item>
            <title>Some other title</title>
            <link>https://somelink.com</link>
            <description>Some desc</description>
            <pubDate>Tue, 10 Jun 2020 23:53:52 +0200</pubDate>
            <guid isPermaLink="false">https://somelink/-/102031/</guid>
        </item>
    </channel>
    </rss>
    """
