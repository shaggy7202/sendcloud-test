from django.views.generic import DetailView
from feed_items.models import FeedItem


class FeedItemDetailView(DetailView):
    model = FeedItem
    template_name = 'feed_items/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.viewed = True
        obj.save()
        return obj
