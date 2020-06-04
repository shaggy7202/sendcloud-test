from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Feed(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('feeds:detail', kwargs={'pk': self.pk})
