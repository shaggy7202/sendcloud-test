from django.views.generic.edit import UpdateView
from feeds.models import Feed


class FeedUpdateView(UpdateView):
    model = Feed
    template_name = 'feeds/update.html'
    fields = ['name']
