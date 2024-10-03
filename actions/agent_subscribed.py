import logging

from .utils.utility import Utility


class AgentSubscribed:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        self.log_info("intent received", str(room_info['id']), conversation)

        if str(room_info['mode']) == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", str(room_info['id']), conversation)
            return []

        # if customer is in the conversation
        if Utility.is_customer_present(conversation):
            Utility.change_bot_participant_role('ASSISTANT', dispatcher, conversation)

        if Utility.THIRD_PARTY_GADGET_ENABLED:
            agent_subscribed = (Utility.get_key(slots, 'cimEvent'))['data']
            Utility.check_and_dispatch_open_gadget_action(conversation, agent_subscribed, dispatcher)

        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[AGENT_SUBSCRIBED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
