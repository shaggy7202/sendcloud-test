from django.views.generic import DeleteView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, redirect
from feed_items.models import Comment


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('feed_items:detail', args=(self.kwargs['feed_item_pk'],))

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        comment = super(CommentDeleteView, self).get_object()
        if not comment.feed_item.feed.created_by.pk == self.request.user.pk:
            raise Http404
        return comment

    def get(self, request, *args, **kwargs):
        # We don't need confirm template for comment deletion
        return redirect('feed_items:detail', pk=self.kwargs['feed_item_pk'])
