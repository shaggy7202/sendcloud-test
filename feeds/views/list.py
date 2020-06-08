from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from feeds.models import Feed


class FeedListView(LoginRequiredMixin, ListView):
    model = Feed
    paginate_by = 20
    template_name = 'feeds/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
