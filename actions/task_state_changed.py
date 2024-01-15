import logging
from .utils.utility import Utility


class TaskStateChanged:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        self.log_info("intent received", str(room_info['id']), conversation)

        if str(room_info['mode']) == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", str(room_info['id']), conversation)
            return []

        task = (Utility.get_key(slots, 'cimEvent'))['data']['task']
        Utility.dispatch_flushed_task_msg(dispatcher, task, 'Your chat has ended due to technical issues. '
                                                            'Please come back later at a convenient time')

        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[TASK_STATE_CHANGED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
