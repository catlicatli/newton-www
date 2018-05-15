#-*- coding: utf-8 -*-
"""Service Implementation of register module
"""
import logging

from django.conf import settings
from django.template import Template, Context, loader
from django.utils.translation import ugettext_lazy as _

from verification import services
from tasks import task_email
from config import codes

logger = logging.getLogger(__name__)


def send_register_validate_email(email, request):
    """Send the validate email for user register
    """
    try:
        # build the email body
        email_type = codes.EmailType.REGISTER.value
        verification = services.generate_verification_uuid(email, email_type)
        if not verification:
            return False
        target_url = "%s/register/verify/?uuid=%s" % (settings.NEWTON_HOME_URL, str(verification.uuid))
        subject = _("Newton Notification: Please complete the register process of Newton")
        template = loader.get_template("register/register-letter.html")
        context = Context({"target_url":target_url,"request":request})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        # send
        task_email.send_email.delay(subject, html_content, from_email, [email])
        return True
    except Exception, inst:
        logger.exception("fail to send the register validate email:%s" % str(inst))
        return False
        
def get_register_verification_by_uuid(uuid):
    """Get the verification object of register by uuid
    """
    return services.get_verification_by_uuid(uuid)
    
    
