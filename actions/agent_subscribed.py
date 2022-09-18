import logging

from .utils.utility import Utility
from .utils.events import slot


class AgentSubscribed:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("AGENT_SUBSCRIBED intent called", conversation_id)

        channel_session_list = Utility.get_channel_sessions(conversation)

        if not channel_session_list:
            self.log_info("Dispatching REVOKE_REQUEST bot-action, Customer has left", conversation_id)
            
            dispatcher.action('REVOKE_REQUEST', {"reasonCode": "CANCELLED"})
            return [slot.set('agent_state', 'not_requested')]

        return [slot.set('agent_state', 'subscribed')]

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_SUBSCRIBED] | conversation = [' + conversation_id + '] - ' + msg)
