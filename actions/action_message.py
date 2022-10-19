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

        agent_state = Utility.get_key(slots, "agent_state", Utility.create_agent_state('not_requested', None))
        routing_mode = Utility.get_routing_mode_from(conversation['channelSession'])

        if name == 'FIND_AGENT':
            if routing_mode != 'PUSH' or agent_state['state'] == 'requested':
                return []
            agent_state = Utility.create_agent_state('requested', 'INBOUND')
            events.append(slot.set("agent_state", agent_state))

        dispatcher.action(name, data)

        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[ACTION_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)
