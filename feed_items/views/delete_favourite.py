from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

from feed_items.models import Favourite


class FavouriteDeleteView(LoginRequiredMixin, View):
    """View for removing feed item from favourites"""

    def post(self, request, pk):
        favourite = get_object_or_404(
            klass=Favourite, pk=pk, feed_item__feed__created_by=request.user
        )
        feed_item_pk = favourite.feed_item.pk
        favourite.delete()
        return redirect('feed_items:detail', pk=feed_item_pk)
