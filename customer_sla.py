import logging
from .utils.utility import Utility
from .utils.webhook import post_channel_session_expired


class CustomerSla:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("Customer activity timer expired", conversation_id)

        channel_session_id = Utility.get_key(slots, 'customer_sla_metadata')
        channel_session = Utility.get_channel_session_by_id(channel_session_id, conversation)

        if channel_session is None:
            self.log_info("ChannelSession not found, will not post channel_session_expired", conversation_id)
        elif not Utility.get_key(Utility.get_key(slots, 'channel_session_sla_map', {}), channel_session['id'], False):
            self.log_info('Customer-activity-timer flag false, will not post channel_session_expired', conversation_id)
        else:
            self.log_info('Posting CHANNEL_SESSION_EXPIRED bot-action', conversation_id)
            post_channel_session_expired(conversation_id, channel_session)

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CUSTOMER_SLA] | conversation = [' + conversation_id + '] - ' + msg)
