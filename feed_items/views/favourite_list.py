from django.views.generic.list import ListView

from feed_items.models import Favourite


class FavouriteListView(ListView):
    template_name = 'feed_items/favourites_list.html'
    model = Favourite
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
