# -*- coding: utf-8 -*-
import logging
from celery import task
import requests
import json
from django.conf import settings

from config import codes
from kyc import models as kyc_models

logger = logging.getLogger(__name__)

@task()
def sync_blockchain_data():
    """Sync the blockchain data
    """
    try:
        for item in kyc_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE, status=codes.KYCStatus.SENT.value):
            # btc
            if item.receive_btc_address:
                txs = __get_btc_transactions(item.receive_btc_address)
                for txid, value in txs:
                    pass
            # ela
            if item.receive_ela_address:
                txs = __get_ela_transactions(item.receive_ela_address)
                for txid, value in txs:
                    pass
    except Exception, inst:
        logger.error("fail to sync blockchain data: %s" % str(inst))

def __get_btc_transactions(address):
    try:
        btc_url = 'https://blockchain.info/rawaddr/%s'
        response = requests.get(btc_url % address)
        data = json.loads(response)
        if data['total_received'] <= 0:
            return []
        txs = data['txs']
        result = []
        for item in txs:
            out = item['out']
            txid = item['hash']
            value = 0
            for tmp_item in out:
                if tmp_item['addr'] == address: # found it
                    value += tmp_item['value']
            if value > 0:
                result.append([txid, value])
        return result
    except Exception, inst:
        logger.exception("fail to get btc transactions:%s" % str(inst))
        return None

def __get_ela_transactions(address):
    try:
        ela_url = 'https://blockchain.elastos.org/api/v1/txs/?address=%s&pageNum=0'
        response = requests.get(ela_url % address)
        data = json.loads(response)
        txs = data['txs']
        result = []
        for item in txs:
            out = item['vout']
            txid = item['txid']
            value = 0
            for tmp_item in out:
                addresses = tmp_item['scriptPubKey']['addresses']
                if address in addresses: # found it
                    value += tmp_item['value']
            if value > 0:
                result.append([txid, value])
        return result
    except Exception, inst:
        logger.exception("fail to get ela transactions:%s" % str(inst))
        return None
