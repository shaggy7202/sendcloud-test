from django.urls import path

from feeds.views import (
    FeedCreateView,
    FeedDetailView,
    FeedDeleteView,
    FeedListView,
    FeedUpdateView,
    FetchItemsForFeedView
)

app_name = 'feeds'
urlpatterns = [
    path('create/', FeedCreateView.as_view(), name='create'),
    path('list/', FeedListView.as_view(), name='list'),
    path('<int:pk>/', FeedDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', FeedUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', FeedDeleteView.as_view(), name='delete'),
    path(
        '<int:pk>/fetch-items/',
        FetchItemsForFeedView.as_view(),
        name='fetch_items'
    ),
]
