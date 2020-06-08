from django import forms

from feed_items.models import Comment


class CreateCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text', 'feed_item')

    def clean_feed_item(self):
        feed_item = self.cleaned_data['feed_item']
        if feed_item and not feed_item.feed.created_by == self.user:
            raise forms.ValidationError(
                "You don't have access to this article"
            )
        return feed_item
