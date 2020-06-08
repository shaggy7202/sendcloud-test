from django.urls import path

from feed_items.views import (
    FeedItemDetailView,
    CommentCreateView,
    CommentDeleteView,
    FavouriteListView,
    FavouriteDeleteView,
    FavouriteCreateView
)


app_name = 'feed_items'
urlpatterns = [
    path('<int:pk>/', FeedItemDetailView.as_view(), name='detail'),
    path('favourites/', FavouriteListView.as_view(), name='favourites_list'),
    path(
        'favourites/create',
        FavouriteCreateView.as_view(),
        name='favourites_create'
    ),
    path(
        'favourites/<int:pk>/delete',
        FavouriteDeleteView.as_view(),
        name='favourites_delete'
    ),
    path(
        'comments/<int:pk>/delete/',
        CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        'comments/create/',
        CommentCreateView.as_view(),
        name='create_comment'
    )
]
