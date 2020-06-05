from django.views.generic import DeleteView
from django.http import Http404
from django.urls import reverse_lazy
from feeds.models import Feed


class FeedDeleteView(DeleteView):
    model = Feed
    template_name = 'feeds/delete.html'
    success_url = reverse_lazy('feeds:list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(FeedDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj
