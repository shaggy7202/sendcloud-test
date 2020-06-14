from django.core.paginator import Paginator
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin

from feeds.models import Feed


@method_decorator(never_cache, 'get')
class FeedDetailView(LoginRequiredMixin, View):
    """View for displaying single feed"""

    def get(self, request, pk):
        feed = get_object_or_404(
            klass=Feed, pk=pk, created_by=self.request.user
        )
        not_viewed_items_count = feed.items.filter(viewed=False).count()
        items = feed.items.all()
        paginator = Paginator(items, 20)  # Show 20 items per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'feed': feed,
            'not_viewed_items_count': not_viewed_items_count,
            'page_obj': page_obj
        }
        return render(request, 'feeds/detail.html', context)
