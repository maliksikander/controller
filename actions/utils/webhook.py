import logging
import requests

API_PATH = "http://ef-conversation-manager-svc.expertflow.svc:8080/controller-webhook"


def post_channel_session_expired(conversation_id, channel_session):
    request_body = {
        "conversationId": conversation_id,
        "messages": [
            {
                "body": {
                    "type": "ACTION",
                    "name": "CHANNEL_SESSION_EXPIRED",
                    "data": {
                        "channelSession": channel_session
                    }
                }
            }
        ]
    }
    post_webhook(request_body, conversation_id, 'channel_session_expired')


def post_webhook(request_body, sender_id, action_name):
    response = requests.post(url=API_PATH, verify=False, json=request_body)
    logging.info('[API_REQUEST] | sender = [' + sender_id + '] - ' + action_name
                 + ' api response = [' + response.text + ']')
