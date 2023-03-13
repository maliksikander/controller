import logging
from .utils.utility import Utility


class ConversationStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

        channel_session = Utility.get_key(slots, 'channelSession')

        bot_id = channel_session['channel']['channelConfig']['botId']
        role = 'PRIMARY'

        dispatcher.action('ASSIGN_BOT', {"botId": bot_id, "role": role})

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CONVERSATION_STARTED] | conversation = [' + conversation_id + '] - ' + msg)
