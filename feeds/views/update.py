from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from feeds.models import Feed


class FeedUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating the feed"""

    model = Feed
    template_name = 'feeds/update.html'
    fields = ['name']
