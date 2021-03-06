"""Urls for the Zinnia entries short link"""
from django.conf.urls import url
from django.conf.urls import patterns

from events.views.shortlink import EntryShortLink


urlpatterns = patterns(
    '',
    url(r'^(?P<token>[\dA-Z]+)/$',
        EntryShortLink.as_view(),
        name='entry_shortlink'),
)
