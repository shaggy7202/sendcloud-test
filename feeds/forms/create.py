from django import forms
from feedparser import parse

from feeds.models import Feed


class CreateFeedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.items = None
        super(CreateFeedForm, self).__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data['url']
        if Feed.objects.filter(created_by=self.user, url=url).exists():
            raise forms.ValidationError('You already have feed for this url')
        return url

    def clean(self):
        cleaned_data = super().clean()

        # Don't need to do additional validation if form has errors
        if self.errors.keys():
            return cleaned_data
        result = parse(cleaned_data['url'])
        self.items = result['entries']

        # Consider url invalid if no entries returned
        if not self.items:
            raise forms.ValidationError('Unable to process given RSS feed url')
        return cleaned_data

    def save(self, commit=True):
        feed = super().save(commit=False)
        feed.created_by = self.user
        if commit:
            feed.save()

            # Save already parsed items for new feed
            feed.items.save_items(feed, self.items)

            # Schedule periodic task for async fetching feed items
            feed.setup_fetcher()
        return feed

    class Meta:
        model = Feed
        fields = ('name', 'url')
