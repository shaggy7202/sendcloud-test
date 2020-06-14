from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from feed_items.models import Favourite


class FavouriteListView(LoginRequiredMixin, ListView):
    """View for displaying list of favourite feed items"""

    template_name = 'feed_items/favourites_list.html'
    model = Favourite
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
