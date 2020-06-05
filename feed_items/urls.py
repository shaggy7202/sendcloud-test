from django.urls import path

from feed_items.views import FeedItemDetailView, CommentDeleteView


app_name = 'feed_items'
urlpatterns = [
    path('<int:pk>/', FeedItemDetailView.as_view(), name='detail'),
    path(
        '<int:feed_item_pk>/comments/<int:pk>/delete/',
        CommentDeleteView.as_view(),
        name='delete_comment'
    )
]
