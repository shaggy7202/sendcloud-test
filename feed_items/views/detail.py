from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from feed_items.forms import CreateCommentForm
from feed_items.models import FeedItem


class FeedItemDetailView(LoginRequiredMixin, DetailView):
    form_class = CreateCommentForm
    template_name = 'feed_items/detail.html'
    model = FeedItem

    def get_object(self, queryset=None):
        obj = super(FeedItemDetailView, self).get_object()
        obj.mark_as_viewed()
        if not obj.feed.created_by == self.request.user:
            raise Http404
        return obj
