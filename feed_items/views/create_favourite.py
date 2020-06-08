from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http.response import HttpResponseNotFound
from feed_items.forms import CreateFavouriteForm


class FavouriteCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = CreateFavouriteForm(user=request.user, data=request.POST)
        if form.is_valid():
            favourite = form.save()
            return redirect('feed_items:detail', pk=favourite.feed_item.pk)

        return HttpResponseNotFound()
