from time import sleep

from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect

from feeds.models import Feed


class FetchItemsForFeedView(LoginRequiredMixin, View):
    """View for manually updating feed items"""

    def get(self, request, pk):
        feed = get_object_or_404(klass=Feed, pk=pk, created_by=request.user)
        lock_id = f'lock-for-feed-{pk}'

        # Trying to get lock and wait if task is running now.
        # Task will be killed after 5 sec in case it freezes.
        while not cache.add(lock_id, "true", timeout=None):
            sleep(1)

        items = feed.fetch_items()
        if items:
            feed.items.save_items(feed, items)
            # Enable fetcher again if update was successful
            feed.enable_fetcher()

        cache.delete(lock_id)
        return redirect('feeds:detail', pk=pk)
