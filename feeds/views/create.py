from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from feeds.forms import CreateFeedForm


class FeedCreateView(LoginRequiredMixin, CreateView):
    """View for creating new feed"""

    form_class = CreateFeedForm
    template_name = 'feeds/create.html'

    def get_form_kwargs(self):
        kwargs = super(FeedCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
