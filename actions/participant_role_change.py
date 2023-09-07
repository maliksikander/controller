import logging
from .utils.utility import Utility


class ParticipantRoleChnage:
    def run(self, conversation, slots, dispatcher, metadata):
        direction = conversation['TopicMetadata']['AgentRequestStatus']['direction']
        if direction == "DIRECT_CONFERENCE":
            dispatcher.action('CANCEL_RESOURCE', {"reasonCode": "CANCELLED"})
            Utility.get_key(slots, 'agent_state', Utility.create_agent_state('not_requested', None))
        elif direction != "DIRECT_TRANSFER":
            for customer_channel_session in Utility.get_channel_sessions(conversation):
                dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": customer_channel_session, "reasonCode": "FORCE_CLOSED"})
        return []


    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CONVERSATION_STARTED] | conversation = [' + conversation_id + '] - ' + msg)
