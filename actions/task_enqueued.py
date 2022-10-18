import logging

from actions.utils.events import slot
from actions.utils.utility import Utility


class TaskEnqueued:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

        task_type = Utility.get_key(slots, 'task')['type']
        direction = str(task_type['direction'])

        if direction == 'DIRECT_TRANSFER' or direction == 'DIRECT_CONFERENCE':
            return [slot.set('agent_state', Utility.create_agent_state('requested', direction))]

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[TASK_ENQUEUED] | conversation = [' + conversation_id + '] - ' + msg)
