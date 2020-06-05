from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from feed_items.models import FeedItem
from feed_items.forms import CreateCommentForm


class FeedItemDetailView(LoginRequiredMixin, FormView):
    form_class = CreateCommentForm
    template_name = 'feed_items/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_item'] = get_object_or_404(
            klass=FeedItem,
            pk=self.kwargs['pk'],
            feed__created_by=self.request.user
        )
        return context

    def get_success_url(self):
        return reverse('feed_items:detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.feed_item_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(FeedItemDetailView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['feed_item_pk'] = self.kwargs['pk']
        return kwargs
