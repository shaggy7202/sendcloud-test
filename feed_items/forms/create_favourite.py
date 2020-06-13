from django import forms

from feed_items.models import Favourite


class CreateFavouriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Favourite
        fields = ('feed_item', )

    def clean_feed_item(self):
        feed_item = self.cleaned_data['feed_item']
        if feed_item.feed.created_by != self.user:
            raise forms.ValidationError("FeedItem doesn't exists")
        return feed_item

    def save(self, commit=True):
        favourite = super().save(commit=False)
        favourite.user = self.user
        if commit:
            favourite.save()
        return favourite
