import logging
from .utils.utility import Utility
from .utils.events import slot


class TaskStateChanged:
    def run(self, conversation, slots, dispatcher, metadata):
        if conversation is None or conversation == {}:
            logging.info("Conversation not found, returning...")
            return []

        task_dto = Utility.get_key(slots, 'taskDto')
        self.log_info("Request received - TaskDto: " + str(task_dto), conversation['id'])

        task_state = task_dto['state']
        if task_state['name'] == 'CLOSED' and task_state['reasonCode'] == 'FORCE_CLOSED':
            dispatcher.text('Your chat has ended due to technical issues. Please come back later at a convenient time')
            return [slot.set('agent_state', Utility.create_agent_state('not_requested', None))]

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[TASK_STATE_CHANGED] | conversation = [' + conversation_id + '] - ' + msg)
