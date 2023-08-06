import os
import datetime
import logging

from django.conf import settings
from firebase_admin import credentials, messaging
from google.oauth2 import service_account

from ..models import Notification

from celery import shared_task

import json
import firebase_admin

# Get an instance of a logger
logger = logging.getLogger(__name__)

"""
https://firebase.google.com/docs/cloud-messaging/auth-server#use-credentials-to-mint-access-tokens
https://github.com/firebase/firebase-admin-python/blob/e35a45a68885d1edfe7a28a2e75a9f1cc444f272/snippets/messaging/cloud_messaging.py
"""

FIREBASE_APP = firebase_admin.initialize_app()
SCOPES = [
        'https://www.googleapis.com/auth/firebase.messaging'
    ]

def get_access_token():
        """
        Retrieve a valid access token that can be used to authorize requests.
        :return: Access token.
        """
        access_token_info = FIREBASE_APP.get_access_token()
        return access_token_info.access_token

@shared_task(name="Non-Periodic: Mobile push notification")
def mobile_push_notification(notification_id):
    notification_obj = Notification.objects.get(id=notification_id)
    # context = json.loads(notification_obj.notification_context)
    devices = notification_obj.user.device_set.all()
    if notification_obj.content is not None:
        for device in devices:
            try:
                message = messaging.Message(
                    token=device.token,
                    notification=messaging.Notification(
                        title=notification_obj.title,
                        body=notification_obj.content,
                        image=notification_obj.image.url if notification_obj.image else '' ,
                    ),
                    android=messaging.AndroidConfig(
                        ttl=datetime.timedelta(seconds=3600),
                        priority='high',
                        notification=messaging.AndroidNotification(
                            icon=notification_obj.icon.url if notification_obj.icon else '' ,
                            default_sound=True,
                            color='#ffffff',
                            default_light_settings=True
                        )
                    ),
                    apns=messaging.APNSConfig(
                        headers={'apns-priority': '10'},
                        payload=messaging.APNSPayload(
                            aps=messaging.Aps(
                                badge=1,
                            ),
                        ),
                    ),
                )
                messaging.send(message)
                logger.info("Push notifiaction sent to device: " + str(device.id))
            except Exception as e:
                logger.warn( "Error sending push notification to device: " + str(device.id) + " message: " + str(e) )

        return "Notifications sent"
    else:
        return "Error Notification has not content"
