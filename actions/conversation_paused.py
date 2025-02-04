import logging

from .utils.utility import Utility

class ConversationPaused:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']

        self.log_info("Dispatching the CONVERSATION_PAUSED message", str(room_info['id']), conversation)
        dispatcher.text('The conversation is currently paused by the agent. We appreciate your patience, '
                        'the agent will get back to you as soon as possible.')

        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[CONVERSATION_PAUSED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)