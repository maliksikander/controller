import logging

from .utils.utility import Utility


class ChannelSessionExpired:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        self.log_info("intent received", str(room_info['id']), conversation)

        channel_session = (Utility.get_key(slots, 'cimEvent'))['data']
        dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": channel_session, "reasonCode": "FORCE_CLOSED"})
        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[CHANNEL_SESSION_EXPIRED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
