from django.urls import path

from feeds.views import FeedCreateView, FeedDetailView, FeedUpdateView

app_name = 'feeds'
urlpatterns = [
    path('create/', FeedCreateView.as_view(), name='create'),
    path('<int:pk>/', FeedDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', FeedUpdateView.as_view(), name='update'),
]
