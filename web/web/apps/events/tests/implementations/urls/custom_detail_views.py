"""Test urls for the zinnia project"""
from django.conf.urls import url
from django.conf.urls import patterns

from events.views.tags import TagDetail
from events.views.authors import AuthorDetail
from events.views.categories import CategoryDetail
from events.tests.implementations.urls.default import (
    urlpatterns as test_urlpatterns)


class CustomModelDetailMixin(object):
    """Mixin for changing the template_name
    and overriding the context"""
    template_name = 'events/entry_custom_list.html'

    def get_context_data(self, **kwargs):
        context = super(CustomModelDetailMixin,
                        self).get_context_data(**kwargs)
        context.update({'extra': 'context'})
        return context


class CustomTagDetail(CustomModelDetailMixin, TagDetail):
    pass


class CustomAuthorDetail(CustomModelDetailMixin, AuthorDetail):
    pass


class CustomCategoryDetail(CustomModelDetailMixin, CategoryDetail):
    pass


urlpatterns = patterns(
    '',
    url(r'^authors/(?P<username>[.+-@\w]+)/$',
        CustomAuthorDetail.as_view(),
        name='events_author_detail'),
    url(r'^authors/(?P<username>[.+-@\w]+)/page/(?P<page>\d+)/$',
        CustomAuthorDetail.as_view(),
        name='events_author_detail_paginated'),
    url(r'^categories/(?P<path>[-\/\w]+)/page/(?P<page>\d+)/$',
        CustomCategoryDetail.as_view(),
        name='events_category_detail_paginated'),
    url(r'^categories/(?P<path>[-\/\w]+)/$',
        CustomCategoryDetail.as_view(),
        name='events_category_detail'),
    url(r'^tags/(?P<tag>[^/]+(?u))/$',
        CustomTagDetail.as_view(),
        name='events_tag_detail'),
    url(r'^tags/(?P<tag>[^/]+(?u))/page/(?P<page>\d+)/$',
        CustomTagDetail.as_view(),
        name='events_tag_detail_paginated'),
) + test_urlpatterns
