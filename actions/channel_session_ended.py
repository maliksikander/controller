import logging

from .utils.utility import Utility
from .utils.events import unschedule, slot


class ChannelSessionEnded:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("CHANNEL_SESSION_ENDED intent received", conversation_id)

        channel_session = Utility.get_key(slots, 'channelSession')
        channel_session_list = Utility.get_channel_sessions(conversation)
        cc_user_list = Utility.get_agents(conversation)
        events = []

        if not channel_session_list:  # Customer left
            agent_state = Utility.get_key(slots, 'agent_state', Utility.create_agent_state('not_requested', None))

            if agent_state['state'] == 'requested':
                self.dispatch_cancel_resource(dispatcher, conversation_id)
                events.append(slot.set('agent_state', Utility.create_agent_state('not_requested', None)))

            if not cc_user_list:  # All agents left
                self.dispatch_end_conversation(dispatcher, conversation_id)
                return [{'type': 'reset'}]

        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        del channel_session_sla_map[channel_session['id']]

        events.append(slot.set('channel_session_sla_map', channel_session_sla_map))
        events.append(unschedule.customer_sla(conversation['id'], channel_session['id']))

        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CHANNEL_SESSION_ENDED] | conversation = [' + conversation_id + '] - ' + msg)

    def dispatch_cancel_resource(self, dispatcher, conversation_id):
        self.log_info("Customer left and Agent was requested, dispatching CANCEL_RESOURCE bot-action", conversation_id)
        dispatcher.action('CANCEL_RESOURCE', {"reasonCode": "CANCELLED"})

    def dispatch_end_conversation(self, dispatcher, conversation_id):
        self.log_info("Customer and Agent(s) left the conversation, ending conversation", conversation_id)
        dispatcher.action('END_CONVERSATION')
