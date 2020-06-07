from time import sleep

from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect

from feeds.models import Feed


class FetchItemsForFeedView(LoginRequiredMixin, View):
    def get(self, request, pk):
        feed = get_object_or_404(klass=Feed, pk=pk, created_by=request.user)
        lock_id = f'lock-for-feed-{pk}'
        # Checking if async update already running and wait if needed.
        # Soft kill after 5 sec
        if cache.get(lock_id):
            sleep(5)

        # Setting lock in case async task failed and will be restarted
        cache.set(lock_id, 'true', timeout=None)

        # Disable fetcher while manually updating the feed
        if feed.fetcher.enabled:
            feed.fetcher.enabled = False
            feed.fetcher.save()

        items = feed.fetch_items()
        if items:
            # Enable fetcher again if update was successful
            feed.items.save_items(feed, items)
            feed.fetcher.enabled = True
            feed.fetcher.save()

        cache.delete(lock_id)
        return redirect('feeds:detail', pk=pk)
