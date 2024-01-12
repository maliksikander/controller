import logging
from .utils.utility import Utility


class TaskStateChanged:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

        room_mode = str((Utility.get_key(slots, 'cimEvent'))['roomInfo']['mode'])

        if room_mode == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", conversation['id'])
            return []

        task = (Utility.get_key(slots, 'cimEvent'))['data']['task']
        Utility.dispatch_flushed_task_msg(dispatcher, task, 'Your chat has ended due to technical issues. '
                                                            'Please come back later at a convenient time')

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[TASK_STATE_CHANGED] | conversation = [' + conversation_id + '] - ' + msg)
