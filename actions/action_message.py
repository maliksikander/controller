import logging
from .utils.utility import Utility
from .utils.events import slot


class ActionMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])
        action_message = Utility.get_key(slots, 'actionMessage')

        name = str(action_message['name'])
        data = action_message['data']

        events = []

        agent_state = Utility.get_key(slots, 'agent_state', "not_requested")
        if name == 'FIND_AGENT':
            if agent_state == 'requested':
                return []
            events.append(slot.set('agent_state', 'requested'))

        dispatcher.action(name, data)
        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[ACTION_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)
