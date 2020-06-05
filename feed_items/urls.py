from django.urls import path

from feed_items.views import FeedItemDetailView


app_name = 'feed_items'
urlpatterns = [
    path('<int:pk>/', FeedItemDetailView.as_view(), name='detail')
]
