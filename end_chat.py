import logging

from .utils.utility import Utility


class EndChat:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        channel_session = Utility.get_latest_channel_session(conversation)

        if channel_session is None:
            self.log_info("ChannelSession not found, will not post channel_session_expired", conversation_id)
        else:
            self.log_info("Posting CHANNEL_SESSION_EXPIRED bot-action", conversation_id)
            dispatcher.action('CHANNEL_SESSION_EXPIRED', {
                "channelSession": channel_session
            })

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[END_CHAT] | conversation = [' + conversation_id + '] - ' + msg)
