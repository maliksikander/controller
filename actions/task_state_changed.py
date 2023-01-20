import logging
from .utils.utility import Utility


class TaskStateChanged:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        task_dto = Utility.get_key(slots, 'taskDto')

        self.log_info("Request received - TaskDto: " + str(task_dto), conversation_id)

        task_state = task_dto['state']
        if task_state['name'] == 'CLOSED' and task_state['reasonCode'] == 'FORCE_CLOSED':
            dispatcher.text('Your chat has ended due to technical issues. Please come back later at a convenient time')

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[TASK_STATE_CHANGED] | conversation = [' + conversation_id + '] - ' + msg)