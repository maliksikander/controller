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

        channel_session = Utility.get_from_list(channel_session_list, channel_session['id'])

        if not channel_session_list and not cc_user_list:
            routing_mode = Utility.get_routing_mode_from(channel_session)
            agent_state = str(Utility.get_key(slots, 'agent_state'))
            self.log_info('Agent state: ' + agent_state, conversation_id)
            
            if routing_mode == 'PUSH' and agent_state == 'requested':
                self.log_info("Agent was requested, dispatching CANCEL_RESOURCE bot-action", conversation_id)
                dispatcher.action('CANCEL_RESOURCE', {"reasonCode": "CANCELLED"})

            dispatcher.action('END_CONVERSATION')
            self.log_info("No channel_sessions and agents left in conversation, restarting tracker", conversation_id)
            return [{'type': 'reset'}]

        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        del channel_session_sla_map[channel_session['id']]

        cancel_timer = unschedule.customer_sla(conversation['id'], channel_session['id'])

        return [cancel_timer, slot.set('channel_session_sla_map', channel_session_sla_map)]

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CHANNEL_SESSION_ENDED] | conversation = [' + conversation_id + '] - ' + msg)
