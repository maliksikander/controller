import logging
from .utils.utility import Utility
from .utils.events import slot



class ParticipantRoleChnage:
    def run(self, conversation, slots, dispatcher, metadata):
        if(Utility.is_all_agent_in_wrap_up(conversation)):
            self.log_info('intent received', conversation['id'])
            direction = str((Utility.get_key(slots, 'cimEvent'))['data']['metadata']['reason'])
            if direction != "DIRECT_TRANSFER":
                for customer_channel_session in Utility.get_channel_sessions(conversation):
                    dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": customer_channel_session, "reasonCode": "FORCE_CLOSED"})
            return []


    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[PARTICIPANT_ROLE_CHANGE] | conversation = [' + str(conversation_id) + '] - ' + msg)
