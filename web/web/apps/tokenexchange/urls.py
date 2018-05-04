# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.show_tokenexchange_index_view),
                       url(r'^post/$', views.post_kyc_information),
                       url(r'^wait-audit/$', views.show_wait_audit_view),
                       url(r'^pending/', views.show_pending_view),
                       url(r'^end/', views.show_end_view),
                       url(r'^apply/$', views.post_apply_amount),
                       url(r'^confirm/$', views.confirm_distribution),
                       
                       url(r'^invalid-link/$', views.show_invalid_link),
                       url(r'^(?P<username>[0-9a-z]+)/$', views.show_receive_address_view),
)
