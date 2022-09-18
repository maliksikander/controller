import logging

from .utils.utility import Utility
from .utils.events import slot


class AgentSubscribed:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("AGENT_SUBSCRIBED intent called", conversation_id)

        channel_sessions = Utility.get_channel_sessions(conversation)

        if not channel_sessions:
            self.log_info("Dispatching REVOKE_REQUEST bot-action, Customer has left", conversation_id)
            
            dispatcher.action('REVOKE_REQUEST', {"reasonCode": "CANCELLED"})
            return [slot.set('agent_state', 'not_requested')]

        bot_participant = Utility.get_bot_participant(conversation)
        if bot_participant is not None and bot_participant['role'] == 'PRIMARY':
            bot_id = bot_participant['participant']['id']
            role = 'ASSISTANT'
            dispatcher.action('CHANGE_PARTICIPANT_ROLE', {"participantId": bot_id, "role": role})

        return [slot.set('agent_state', 'subscribed')]

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_SUBSCRIBED] | conversation = [' + conversation_id + '] - ' + msg)
