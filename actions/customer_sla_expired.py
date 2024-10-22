import logging

from .utils.utility import Utility


class CustomerSlaExpired:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']

        channel_session = slots['channelSession']
        dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": channel_session, "reasonCode": "FORCE_CLOSED"})
        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[Customer_SLA_EXPIRED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)

