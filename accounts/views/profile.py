from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from feeds.models import Feed


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['created_feeds'] = Feed.objects.filter(
            created_by=self.request.user
        )
        return context
