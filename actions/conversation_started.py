import logging
from .utils.utility import Utility


class ConversationStarted:
    def run(self, conversation, slots, dispatcher, metadata):

        channel_session = Utility.get_key(slots, 'channelSession')

        if Utility.get_key(channel_session, 'latestIntent') == 'START_CONVERSATION':
            self.log_info("Latest intent is equal to 'START_CONVERSATION', bot will not be added", conversation['id'])
            return []

        mrd_id = channel_session['channel']['channelType']['mediaRoutingDomain']

        # Bot is not added for voice channels.
        if mrd_id == '62f9e360ea5311eda05b0242' or mrd_id == '20316843be924c8ab4f57a7a':
            self.log_info("Channel is of voice type, bot will not be added in conversation.", conversation['id'])
            return []

        bot_id = channel_session['channel']['channelConfig']['botId']
        role = 'PRIMARY'

        dispatcher.action('ASSIGN_BOT', {"botId": bot_id, "role": role})

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CONVERSATION_STARTED] | conversation = [' + conversation_id + '] - ' + msg)
