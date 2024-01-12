import logging

from .utils.utility import Utility


class AgentSubscribed:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

        room_mode = str((Utility.get_key(slots, 'cimEvent'))['roomInfo']['mode'])

        if room_mode == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", conversation['id'])
            return []

        # if customer is in the conversation
        if Utility.is_customer_present(conversation):
            Utility.change_bot_participant_role('ASSISTANT', dispatcher, conversation)

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_SUBSCRIBED] | conversation = [' + conversation_id + '] - ' + msg)
