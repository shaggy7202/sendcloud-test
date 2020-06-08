from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http.response import HttpResponseNotFound

from feed_items.forms import CreateCommentForm


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = CreateCommentForm(
            user=request.user, data=request.POST
        )
        if form.is_valid():
            comment = form.save()
            return redirect('feed_items:detail', pk=comment.feed_item.pk)
        return HttpResponseNotFound()
