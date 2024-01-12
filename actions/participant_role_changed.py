import logging
from .utils.utility import Utility


class ParticipantRoleChanged:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info('intent received', conversation['id'])

        room_mode = str((Utility.get_key(slots, 'cimEvent'))['roomInfo']['mode'])

        if room_mode == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", conversation['id'])
            return []

        if Utility.is_all_agent_in_wrap_up(conversation):
            direction = str((Utility.get_key(slots, 'cimEvent'))['data']['metadata']['reason'])
            if direction != "DIRECT_TRANSFER":
                self.log_info("All agents in wrap-up, and direction is not direct-transfer, removing channel sessions",
                              conversation['id'])
                for customer_channel_session in Utility.get_channel_sessions(conversation):
                    dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": customer_channel_session,
                                                                 "reasonCode": "FORCE_CLOSED"})
            return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[PARTICIPANT_ROLE_CHANGE] | conversation = [' + str(conversation_id) + '] - ' + msg)
