import logging

from .utils.utility import Utility


class Default:
    def run(self, conversation, slots, dispatcher, metadata):
        room_id = str((Utility.get_key(slots, 'cimEvent'))['roomInfo']['id'])
        self.log_info("Default action called", room_id, conversation)
        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info('[Default] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
