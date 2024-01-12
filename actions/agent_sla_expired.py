import logging
from .utils.utility import Utility


class AgentSlaExpired:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

        room_mode = str((Utility.get_key(slots, 'cimEvent'))['roomInfo']['mode'])

        if room_mode == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", conversation['id'])
            return []

        agent_participants = Utility.get_conversation_participants(conversation, 'AGENT')
        dispatcher.action('REMOVE_ALL_AGENTS', {"agentParticipants" : agent_participants})

        return[]


    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_SLA_EXPIRED] | conversation = [' + conversation_id + '] - ' + msg)