from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from feed_items.models import Comment


class CommentDeleteView(LoginRequiredMixin, View):
    """View for deleting the comment"""

    def post(self, request, pk):
        comment = get_object_or_404(
            klass=Comment, pk=pk, feed_item__feed__created_by=request.user
        )
        feed_item_pk = comment.feed_item.pk
        comment.delete()
        return redirect('feed_items:detail', pk=feed_item_pk)
