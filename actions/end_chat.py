import logging

from .utils.utility import Utility


class EndChat:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        channel_session = Utility.get_latest_channel_session(conversation)

        if channel_session is None:
            self.log_info("ChannelSession not found, will not post REMOVE_CHANNEL_SESSION", conversation_id)
            return []

        self.log_info("Posting REMOVE_CHANNEL_SESSION bot-action", conversation_id)
        dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": channel_session, "reasonCode": "FORCE_CLOSED"})
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[END_CHAT] | conversation = [' + conversation_id + '] - ' + msg)
