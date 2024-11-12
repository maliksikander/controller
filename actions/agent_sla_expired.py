import logging
from .utils.utility import Utility


class AgentSlaExpired:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']

        if str(room_info['mode']) == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", str(room_info['id']), conversation)
            return []

        agent_participants = Utility.get_conversation_participants(conversation, 'AGENT')
        dispatcher.action('REMOVE_ALL_AGENTS', {"agentParticipants": agent_participants, "reason": "SLA_EXPIRED"})

        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[AGENT_SLA_EXPIRED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
