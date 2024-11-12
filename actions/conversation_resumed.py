import logging

from .utils.utility import Utility

class ConversationResumed:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']

        reason = str((Utility.get_key(slots, 'cimEvent'))['data'])


        if reason not in ["AGENT_MESSAGE", "SYSTEM"]:
            self.log_info("Dispatching the CONVERSATION_RESUMED message", str(room_info['id']), conversation)
            dispatcher.text('The conversation is resumed now.')

        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[CONVERSATION_RESUMED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)