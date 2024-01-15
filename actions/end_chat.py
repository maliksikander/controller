import logging

from .utils.utility import Utility


class EndChat:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        self.log_info("intent received", str(room_info['id']), conversation)

        if str(room_info['mode']) == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", str(room_info['id']), conversation)
            return []

        channel_session = Utility.get_latest_channel_session(conversation)

        if channel_session is None:
            self.log_info("ChannelSession not found, will not post REMOVE_CHANNEL_SESSION", str(room_info['id']),
                          conversation)
            return []

        self.log_info("Posting REMOVE_CHANNEL_SESSION bot-action", str(room_info['id']), conversation)
        dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": channel_session, "reasonCode": "FORCE_CLOSED"})
        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info('[END_CHAT] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
