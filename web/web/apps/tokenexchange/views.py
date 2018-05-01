# -*- coding: utf-8 -*-
import logging
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import utc

import decorators
from utils import http
from config import codes
from . import forms
from . import services
from . import models as tokenexchange_models

logger = logging.getLogger(__name__)

def exchange_valid_required(func):
    """
    """
    def _decorator(request, *args, **kwargs):
        now = datetime.datetime.now()
        if now < settings.FUND_START_DATE:
            return redirect('/tokenexchange/pending/')
        elif now > settings.FUND_END_DATE:
            return redirect('/tokenexchange/end/')
        else:
            return func(request, *args, **kwargs)
    return _decorator

@exchange_valid_required
@login_required
def show_tokenexchange_index_view(request):
    return render(request, "tokenexchange/index.html", locals()) 

@exchange_valid_required
@login_required
def show_join_tokenexchange_view(request):
    instance = tokenexchange_models.KYCInfo.objects.filter(user=request.user, phase_id=settings.CURRENT_FUND_PHASE).first()
    form = forms.KYCInfoForm(instance=instance)
    return render(request, "tokenexchange/submit.html", locals()) 

@exchange_valid_required
@login_required
@decorators.http_post_required
def post_kyc_information(request):
    try:
        # TODO twice submit tokenexchange info need check.
        form = forms.KYCInfoForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "tokenexchange/submit.html", locals())
        # check whether user is submit kyc info
        instance = tokenexchange_models.KYCInfo.objects.filter(user=request.user, phase_id=settings.CURRENT_FUND_PHASE).first()
        instance = form.save(commit=False)
        instance.phase_id = settings.CURRENT_FUND_PHASE
        instance.user = request.user
        instance.save()
        email = request.user.email
        services.send_kyc_confirm_email(email, request)
        return redirect('/tokenexchange/wait-audit/')
    except Exception, inst:
        logger.exception("fail to post kyc information:%s" % str(inst))
        return http.HttpResponseServerError()

@exchange_valid_required
@login_required
def show_wait_audit_view(request):
    return render(request, "tokenexchange/wait-audit.html", locals())

def verify_email_link(request):
    try:
        uuid = request.GET['uuid']
        verification = services.get_kyc_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/tokenexchange/invalid-link/')
            #check link status
        verification_status = verification.status
        if verification_status != codes.StatusCode.AVAILABLE.value:
            return http.HttpResponseRedirect('/tokenexchange/invalid-link/')
        email = verification.email_address
        expire_time = verification.expire_time
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        # don't check whether the given link is expired
        #if now > expire_time:
            #return http.HttpResponseRedirect('/tokenexchange/invalid-link/')
        return http.HttpResponseRedirect('/tokenexchange/limit-address/?uuid=%s' %str(uuid))
    except Exception, inst:
        logger.exception('fail to verify email link: %s' % str(inst))
        return http.HttpResponseServerError()
        
    return render(request, "tokenexchange/wait-audit.html", locals())

def show_limit_and_address_view(request):
    uuid = request.GET['uuid']
    verification = services.get_kyc_verification_by_uuid(uuid)
    if not verification:
        return http.HttpResponseRedirect('/tokenexchange/invalid-link/')
        #check link status
    verification_status = verification.status
    if verification_status != codes.StatusCode.AVAILABLE.value:
        return http.HttpResponseRedirect('/tokenexchange/invalid-link/')
    email = verification.email_address
    user = User.objects.filter(email=email).first()
    if not user:
        return http.HttpResponseRedirect('/tokenexchange/invalid-link/')
    kycinfo = tokenexchange_models.KYCInfo.objects.filter(user=user).first()
    if not kycinfo:
        return http.HttpResponseRedirect('/tokenexchange/invalid-link/')
    form = forms.KYCAddressForm(instance=kycinfo)
    return render(request, "tokenexchange/limit-address.html", locals())

def show_invalid_link(request):
    return render(request, "tokenexchange/invalid-link.html", locals())
    
@login_required
def show_receive_address_view(request, username):
    try:
        user = User.objects.get(username=username)
        item = tokenexchange_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE, user=user).first()
        return render(request, "tokenexchange/receive-address.html", locals())
    except Exception, inst:
        logger.exception("fail to show receive address:%s" % str(inst))
        return http.HttpResponseServerError()
 
def show_pending_view(request):
    return render(request, "tokenexchange/pending.html", locals())

def show_end_view(request):
    return render(request, "tokenexchange/end.html", locals())

@login_required
def post_apply_amount(request):
    """ Post the amount of apply
    """
    try:
        item = tokenexchange_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE, user=user).first()
        if not item:
            return http.HttpResponseServerError()
        if request.method == 'POST':
            form = forms.ApplyAmountForm(request.POST)
            if form.is_valid():
                item.expect_btc = form.cleaned_data['expect_btc']
                item.expect_ela = form.cleaned_data['expect_ela']
                item.status = codes.TokenExchangeStatus.APPLY_AMOUNT.value
                item.save()
                return render(request, "tokenexchange/apply-success.html", locals())
        else:
            form = forms.ApplyAmountForm()
        return render(request, "tokenexchange/apply-amount.html", locals())
    except Exception, inst:
        logger.exception("fail to post the apply amount:%s" % str(inst))
        return http.HttpResponseServerError()

@login_required
def confirm_distribution(request):
    """ Confirm the distribution of amount
    """
    try:
        item = tokenexchange_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE, user=user).first()
        if not item:
            return http.HttpResponseServerError()
        if request.method == 'POST':
            form = forms.ApplyAmountForm(request.POST)
            if form.is_valid():
                item.status = codes.TokenExchangeStatus.CONFIRM_DISTRIBUTION.value
                item.save()
                return render(request, "tokenexchange/confirm-distribution-success.html", locals())
        else:
            form = forms.ApplyAmountForm()
        return render(request, "tokenexchange/confirm-distribution.html", locals())
    except Exception, inst:
        logger.exception("fail to confirm distribution:%s" % str(inst))
        return http.HttpResponseServerError()
