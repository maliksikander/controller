import logging

from .utils.utility import Utility


class ChannelSessionExpired:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])
        channel_session = (Utility.get_key(slots, 'cimEvent'))['data']
        dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": channel_session, "reasonCode": "FORCE_CLOSED"})
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CHANNEL_SESSION_EXPIRED] | conversation = [' + conversation_id + '] - ' + msg)
