from django import forms

from feed_items.models import Comment, FeedItem


class CreateCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.feed_item_pk = kwargs.pop('feed_item_pk')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text', )
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    def clean(self):
        cleaned_data = super().clean()
        try:
            feed_item = FeedItem.objects.get(pk=self.feed_item_pk)
        except FeedItem.DoesNotExist:
            raise forms.ValidationError("FeedItem doesn't exists")
        if feed_item.feed.created_by.pk != self.user.pk:
            raise forms.ValidationError(
                "You can't leave comments for this item"
            )
        return cleaned_data
