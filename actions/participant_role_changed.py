import logging
from .utils.utility import Utility


class ParticipantRoleChanged:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        self.log_info("intent received", str(room_info['id']), conversation)

        if str(room_info['mode']) == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", str(room_info['id']), conversation)
            return []

        if Utility.is_all_agent_in_wrap_up(conversation):
            direction = str((Utility.get_key(slots, 'cimEvent'))['data']['metadata']['reason'])
            if direction != "DIRECT_TRANSFER" and direction != "CONSULT_TRANSFER":
                self.log_info("All agents in wrap-up, and direction is not direct-transfer, removing channel sessions",
                              str(room_info['id']), conversation)
                for customer_channel_session in Utility.get_channel_sessions(conversation):
                    dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": customer_channel_session,
                                                                 "reasonCode": "AGENT"})
        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[PARTICIPANT_ROLE_CHANGED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
