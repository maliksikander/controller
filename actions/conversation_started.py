import logging
from .utils.utility import Utility


class ConversationStarted:
    def run(self, conversation, slots, dispatcher, metadata):

        channel_session = Utility.get_key(slots, 'channelSession')

        if Utility.get_key(channel_session, 'latestIntent') == 'START_CONVERSATION':
            self.log_info("Latest intent is equal to 'START_CONVERSATION', bot will not be added", conversation['id'])
            return []

        bot_id = channel_session['channel']['channelConfig']['botId']
        role = 'PRIMARY'

        dispatcher.action('ASSIGN_BOT', {"botId": bot_id, "role": role})

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CONVERSATION_STARTED] | conversation = [' + conversation_id + '] - ' + msg)
