from django.views.generic import DetailView
from feeds.models import Feed


class FeedDetailView(DetailView):
    model = Feed
    template_name = 'feeds/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
