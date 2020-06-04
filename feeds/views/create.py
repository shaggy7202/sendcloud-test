from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from feeds.models import Feed


class FeedCreateView(CreateView):
    model = Feed
    fields = ['name', 'url']
    template_name = 'feeds/create.html'

    def form_valid(self, form):
        feed = form.save(commit=False)
        feed.created_by = self.request.user
        feed.save()
        self.object = feed
        return redirect(feed.get_absolute_url())
