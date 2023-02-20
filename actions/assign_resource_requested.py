import logging
from .utils.utility import Utility
from .utils.events import slot


class AssignResourceRequested:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']

        request_payload = Utility.get_key(slots, 'assignResourceRequestDto')
        self.log_info("Request received - payload: " + str(request_payload), conversation_id)

        agent_state = Utility.get_key(slots, "agent_state", Utility.create_agent_state('not_requested', None))
        routing_mode = Utility.get_routing_mode_from(conversation['channelSession'])

        if routing_mode != 'PUSH' or agent_state['state'] == 'requested':
            return []

        dispatcher.action('FIND_AGENT', self.get_find_agent_data(request_payload['queue']))

        queue = request_payload['queue']
        if queue:
            dispatcher.action('FIND_AGENT', Utility.get_find_agent_payload(queue['name'], queue['type'], False))
        else:
            dispatcher.action('FIND_AGENT', Utility.get_find_agent_payload(None, None, False))

        return [slot.set("agent_state", Utility.create_agent_state('requested', 'INBOUND'))]

    @staticmethod
    def get_find_agent_data(queue):
        if queue:
            return {"queue": queue['name'], "type": queue['type']}
        return None

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[ASSIGN_RESOURCE_REQUESTED] | conversation = [' + conversation_id + '] - ' + msg)
